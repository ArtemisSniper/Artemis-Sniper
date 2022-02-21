import requests
from colorama import Fore
import msmcauth
import socket
import ssl
import datetime
import threading
import time
from rich.console import Console
from rich.table import Table
from discord_webhook import DiscordWebhook, DiscordEmbed
import fade

table = Table(title="\nAcc Session Info")
console = Console()
webhook_link = ""
MAX_USAGE = 4  # set the maximum usage for each token
GC_USAGE = 2

#Limit Requests Per Token
class TokenWrapper:
    def __init__(self, token):
        self.token = token
        self.usage = 0  # 0 has not been used yet

    def get_token(self):
        self.usage += 1  # add 1 to usage when a request is used (per request)
        return self.token

accounts = {f"{prefix}_accounts": [] for prefix in ('valid', 'invalid', 'blocked', 'microsoft', 'gc', 'all', 'gmail')}

#Bools
NameChangeYN = False
license_file_exists = False
Success = False
#Req Lists
delays = []
receives = []
readable_date = []


def droptimeApi(name):
    req = requests.get(f"http://api.star.shopping/droptime/{name}", headers={"User-Agent": "Sniper"})
    if req.status_code == 200:
        return req.json()["unix"]

def auto_ping(num_ping):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
        so.connect(('api.minecraftservices.com', 443))
        context = ssl.create_default_context()
        ssock = context.wrap_socket(
            so, server_hostname='api.minecraftservices.com')
        for _ in range(num_ping):
            start = time.time()
            ssock.send(bytes("PUT /minecraft/profile/name/TEST HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer " + "TEST_TOKEN\r\n\r\n", "utf-8"))
            ssock.recv(10000).decode('utf-8')
            end = time.time()
            delays.append(end - start)
        auto_offset = int((sum(delays) / len(delays) * 1000 / 2) + 10)
    return auto_offset


#Mojang Name Change EP requests
def send_request(output):
    # With closes socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('api.minecraftservices.com', 443))
        context = ssl.create_default_context()
        ss = context.wrap_socket(
            s, server_hostname='api.minecraftservices.com')
    for tw in accounts['valid_accounts']:
        while tw.usage < MAX_USAGE:
            ss.send(bytes(f'{initial} {tw.get_token()}\r\n\r\n', 'utf-8'))
            output.append((ss.recv(423), time.time()))

#GiftCard Name Change EP requests
def gc_send_request(output):
    #With closes socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('api.minecraftservices.com', 443))
        context = ssl.create_default_context()
        ss = context.wrap_socket(
            s, server_hostname='api.minecraftservices.com')
    for gw in accounts['gc_accounts']:
        while gw.usage < GC_USAGE:
            ss.send(bytes(f'{initial} {gw.get_token()}\r\n\r\n', 'utf-8'))
            output.append((ss.recv(423), time.time()))

#Microsoft Name Change EP requests
def ms_send_request(output):
    # With closes socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('api.minecraftservices.com', 443))
        context = ssl.create_default_context()
        ss = context.wrap_socket(
            s, server_hostname='api.minecraftservices.com')
    for mw in accounts['microsoft_accounts']:
        while mw.usage < MAX_USAGE:
            ss.send(bytes(f'{initial} {mw.get_token()}\r\n\r\n', 'utf-8'))
            output.append((ss.recv(423), time.time()))

def thread_send_reqs(count):
    responses = []
    threads = [threading.Thread(target=send_request, args=(
            responses,)) for _ in range(count)]
    for t in threads:
        t.start()
    t.join()
    return responses

def ms_thread_send_reqs(count):
    responses = []
    threads = [threading.Thread(target=ms_send_request, args=(
            responses,)) for _ in range(count)]
    for t in threads:
        t.start()
    t.join()
    return responses


def gc_thread_send_reqs(count):
    responses = []
    threads = [threading.Thread(target=gc_send_request, args=(
            responses,)) for _ in range(count)]
    for t in threads:
        t.start()
    t.join()
    return responses


def success_true(token_list):
    global Success
    threads = threading.active_count() - 1
    while threads:
        threads = threading.active_count() - 1
        print(f"Waiting for {threads} thread(s) to finish...")
        time.sleep(0.5) #Wait until threads terminate
    #Sort Times
    output.sort(key=lambda sorts: sorts[1])
    for outs in output:
        statusCode = outs[0].decode("utf-8")[9:12]
        print(f"Recv: {statusCode} @ {datetime.datetime.utcfromtimestamp(outs[1]).strftime('%S.%f')}")
        if statusCode.isnumeric() and int(statusCode) == 200:
            Success = True
    if Success:
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/icons/944338449140420690/eaf9e293982fe84b1bb5ff08f40a17f9.webp?size=1024')
        webhook.add_embed(embed)
        webhook.execute()
        for token in token_list:
            username = requests.get(
                "https://api.minecraftservices.com/minecraft/profile",
                headers={"Authorization": "Bearer " + token.get_token()},
            ).json()["name"]
            if username == target_name:
                skin_change = requests.post(
                    "https://api.minecraftservices.com/minecraft/profile/skins",
                    json={
                        "variant": "classic",
                        "url": "https://i.imgur.com/8nuxlIk.png",
                    },
                    headers={"Authorization": "Bearer " + token.get_token()},
                )
                if skin_change.status_code == 200:
                    print(f"{Fore.MAGENTA}Successfully delivered Skin Change{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}Failed to deliver Skin Change{Fore.RESET}")
                print(f"{Fore.MAGENTA}Sniped {Fore.RESET}{target_name}")

#Check for Dups accs
with open("accs.txt", mode="r") as file:
    data = file.read()

words = data.replace("\n", " ").split()

found_words = set()  # no order.
filtered_words = []  # keeps insertion order.
for i in words:
   if i not in found_words:
      filtered_words.append(i)
      found_words.add(i)

in_string = "\n".join(filtered_words)

with open("accs.txt", mode="w") as file:
   file.write(in_string)

#Start main
print(fade.purplepink(f"""
##########                #                #########   ######   ########## 
     # ##  #########   #######  ##########         #     #      #        # 
     #     #       #    # #             #          # ##########         #  
    #      #       #    # #            #   ########      #             #   
   #       #       # ##########     # #           #      #            #    
  #        #########      #          #            #      #          ##     
 #                        #           #    ########       ####    ##    
                                                     e v e r e s t
"""))
print("Blessed by the Goddess - Artemis\n")

print("[Name To Snipe] [Offset]\n")
code = input("|)-> ").split()
offset = 0
while len(code) < 1:
    code = input("invalid format |)-> ").split()
pinger = auto_ping(5)

if len(code) < 2:
    #auto offset
    print(f"\nOffset not specified, received: {pinger}ms\n")
    tune_delay = input("Tune Delay (press enter if false) -> ")
    if len(tune_delay) < 1:
        offset = float(pinger) / 1000
    else:
        offset = float(tune_delay) / 1000

target_name = code[0]
droptime = (droptimeApi(target_name) - offset)

#Authentication Proccess
with open('accs.txt', 'r') as f:
    #Ignore Spaces in text file
    lines = list(filter(lambda i: i, list(map(lambda s: s.strip("\n"), f.readlines()))))

with open("accs.txt") as file:
    for line in file.read().splitlines():
        if not line.strip():
            continue
        splitter = line.split(":")

        try:
            authentication = requests.post("https://authserver.mojang.com/authenticate",
                                           json={"username": splitter[0], "password": splitter[1]})
        except IndexError:
            print("Please Provide your password")
            exit()
        if "Request blocked" in authentication.text:
            print(
                f"[{Fore.LIGHTRED_EX}{authentication.status_code}{Fore.RESET}] {splitter[0]} {Fore.LIGHTRED_EX}Blocked{Fore.RESET}")
            accounts['blocked_accounts'].append(authentication.status_code)
            if len(accounts['blocked_accounts']) == 4:
                print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Consider Switching your Ip to Authenticate Accounts")
                pass
            elif len(accounts['blocked_accounts']) >= 9:
                print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Switch your Ip to continue Authenticating your Accounts")
                break
        # microsoft
        elif authentication.status_code == 410:
            print(
                f"[{Fore.GREEN}{authentication.status_code}{Fore.RESET}] {splitter[0]} {Fore.RESET}", end="")
            try:
                msresps = msmcauth.login(splitter[0], splitter[1])
                msresp = msresps.access_token
                print(f"\r{Fore.MAGENTA}Successfully Logged into {msresps.username} {Fore.RESET}\n", end="")
            except:
                print("[skip]")
                msresp = input("\nLogin Failed, Enter Token Manually -> ")

            profile = requests.get("https://api.minecraftservices.com/minecraft/profile",
                                   headers={"Authorization": "Bearer " + msresp}).json()
            reedeem = requests.put("https://api.minecraftservices.com/productvoucher/:voucher", headers={
                "Content-type": "application/json",
                "Authorization": "Bearer " + msresp,
            })
            if profile.get("name"):
                accounts['all_accounts'].append("ms")
                accounts['microsoft_accounts'].append(TokenWrapper(msresp))
                continue
            else:
                if reedeem.status_code == "200":
                    print("Successfully redeemed Product Voucher")
                    accounts['all_accounts'].append("gc")
                    accounts['gc_accounts'].append(TokenWrapper(msresp))
                    pass
                elif reedeem.json()["errorMessage"] == "The server has not found anything matching the request URI":
                    print("Product Voucher is already reedemed, continuing")
                    accounts['all_accounts'].append("gc")
                    accounts['gc_accounts'].append(TokenWrapper(msresp))
                else:
                    print(f"Failed to redeem Product Voucher [{Fore.MAGENTA}{reedeem.status_code}{Fore.RESET}]")
                    accounts['invalid_accounts'].append("product")

        elif authentication.status_code == 403:
            print(
                f"[{Fore.LIGHTRED_EX}{authentication.status_code}{Fore.RESET}] {splitter[0]} {Fore.RESET}\n", end="")
            try:
                msresps = msmcauth.login(splitter[0], splitter[1])
                msresp = msresps.access_token
                print(f"{Fore.GREEN}Successfully Logged into {msresps.username} {Fore.RESET}")
                profile = requests.get("https://api.minecraftservices.com/minecraft/profile",
                                       headers={"Authorization": "Bearer " + msresp}).json()
                reedeem = requests.put("https://api.minecraftservices.com/productvoucher/:voucher", headers={
                    "Content-type": "application/json",
                    "Authorization": "Bearer " + msresp,
                })
                if profile.get("name"):
                    accounts['all_accounts'].append("ms")
                    accounts['microsoft_accounts'].append(TokenWrapper(msresp))
                    continue
                else:
                    if reedeem.status_code == "200":
                        print("Successfully redeemed Product Voucher")
                        accounts['all_accounts'].append("gc")
                        accounts['gc_accounts'].append(TokenWrapper(msresp))
                        pass
                    elif reedeem.json()["errorMessage"] == "The server has not found anything matching the request URI":
                        print("Product Voucher is already reedemed, continuing")
                        accounts['all_accounts'].append("gc")
                        accounts['gc_accounts'].append(TokenWrapper(msresp))
                    else:
                        print(f"Failed to redeem Product Voucher [{Fore.MAGENTA}{reedeem.status_code}{Fore.RESET}]")
                        accounts['invalid_accounts'].append("product")
            except:
                accounts['invalid_accounts'].append("invalid_mojang")

        else:
            if authentication.json().get("accessToken") is None:
                print(f"[{Fore.LIGHTRED_EX}{authentication.status_code}{Fore.RESET}] {splitter[0]}")
                accounts['invalid_accounts'].append(authentication.status_code)
            elif "accessToken" in authentication.json():
                token = {"Authorization": "Bearer " + authentication.json()["accessToken"]}
                name_change_allow = requests.get(
                    "https://api.minecraftservices.com/minecraft/profile/namechange",
                    headers=token,
                )
                if name_change_allow.json()["nameChangeAllowed"] == True:
                    NameChangeYN = True
                    print(f"[{Fore.GREEN}{name_change_allow.status_code}{Fore.RESET}] {splitter[0]} Name Change Allowed")
                    sec_question = requests.get(
                        "https://api.mojang.com/user/security/location",
                        headers=token,
                    )
                    if sec_question.status_code == "403":
                        getsec_question = requests.get(
                            "https://api.mojang.com/user/security/challenges",
                            headers=token,
                        )
                        x = getsec_question.json()

                        if len(x) > 0:
                            print("Security Questions are required")
                            for q in x:
                                print(q["question"]["question"])
                            xe = [q["answer"]["id"] for q in x]
                            secquestions_payload = [
                                {"id": int(xe[0]), "answer": splitter[2]},
                                {"id": int(xe[1]), "answer": splitter[3]},
                                {"id": int(xe[2]), "answer": splitter[4]},
                            ]
                            sec_post = requests.post(
                                "https://api.mojang.com/user/security/location",
                                json=secquestions_payload,
                                headers=token,
                            )
                            sec_post_status = str(sec_post.status_code)
                            print(f"[{sec_post_status}]")
                            if sec_post_status == "204":
                                print(
                                    f"{Fore.GREEN}Successfully logged in and whitelisted sec questions{Fore.RESET}"
                                )
                                accounts['valid_accounts'].append(TokenWrapper(authentication.json()["accessToken"]))
                                accounts['all_accounts'].append("valid")
                            else:
                                print(
                                    f"{Fore.LIGHTRED_EX}Failed to whitelist please put in the correct security question credentials in accs.txt{Fore.RESET}")
                    else:
                        accounts['valid_accounts'].append(TokenWrapper(authentication.json()["accessToken"]))
                        accounts['all_accounts'].append("valid")
                else:
                    print(
                        f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] [{Fore.LIGHTRED_EX}{name_change_allow.status_code}{Fore.RESET}] {splitter[0]} Can not name change")
                    accounts['invalid_accounts'].append("invalid")


if not accounts['all_accounts']:
    print("No accounts Valid...")
    exit()
else:
    table.add_column("Account Types", style="cyan")
    table.add_column("Amount", style="magenta")
    table.add_row("Valid Accounts", f"[{len(accounts['all_accounts'])}]", style="green")
    table.add_row("Invalid Accounts", f"[{len(accounts['invalid_accounts'])}]", style="red")
    table.add_row("Mojang Accounts", f"[{len(accounts['valid_accounts'])}]")
    table.add_row("Microsoft Accounts", f"[{len(accounts['microsoft_accounts'])}]")
    table.add_row("Giftcard Accounts", f"[{len(accounts['gc_accounts'])}]")
    console.print(table)
#Webhook
webhook = DiscordWebhook(url=f'{webhook_link}', rate_limit_retry=True)
embed = DiscordEmbed(title="NameMC", url=f'https://namemc.com/search?q={target_name}',
                     description=f"**Sniped `{target_name}` :ok_hand:**", color=12282401)
#Prepare Sleep
time.sleep((droptime - time.time()))

if accounts['gc_accounts']:
    initial =  f"POST /minecraft/profile HTTP/1.1\r\nHost: api.minecraftservices.com\r\nprofileName: {target_name}\r\nAuthorization: Bearer "
    output = gc_thread_send_reqs(len(accounts['gc_accounts'] * 2))
    success_true(accounts['gc_accounts'])

elif accounts['microsoft_accounts']:
    initial = f"PUT /minecraft/profile/name/{target_name} HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer "
    output = ms_thread_send_reqs(len(accounts['microsoft_accounts']*4))
    success_true(accounts['microsoft_accounts'])

elif accounts['valid_accounts']:
    initial = f"PUT /minecraft/profile/name/{target_name} HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer "
    output = thread_send_reqs(len(accounts['valid_accounts']*4))
    success_true(accounts['valid_accounts'])
