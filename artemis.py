import requests
from colorama import Fore
import msmcauth
import socket
import ssl
import datetime
import threading
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import fade

WEBHOOK = ""
accdata = []
delays = []
output = []
#Tools
def droptimeApi(name):
    req = requests.get(f"http://api.star.shopping/droptime/{name}", headers={"User-Agent": "Sniper"})
    if req.status_code == 200:
        return req.json()["unix"]

def NameChange(bearer):
    return requests.get(
            "https://api.minecraftservices.com/minecraft/profile/namechange",
            headers={"Authorization": "Bearer " + bearer},
        ).json()["nameChangeAllowed"]

def auto_ping(num_ping):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
        so.connect(('api.minecraftservices.com', 443))
        context = ssl.create_default_context()
        ssock = context.wrap_socket(
            so, server_hostname='api.minecraftservices.com')
        for _ in range(num_ping):
            start = time.time()
            ssock.send(bytes(
                "PUT /minecraft/profile/name/TEST HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer " + "TEST_TOKEN\r\n\r\n",
                "utf-8"))
            ssock.recv(10000).decode('utf-8')
            end = time.time()
            delays.append(end - start)
        auto_offset = int((sum(delays) / len(delays) * 1000 / 2) + 10)
    return auto_offset

def countdown_time(count_amt: float) -> None:
    for count_amt in range(int(count_amt), 0, -1):
        mins, secs = divmod(count_amt, 99999)
        print(f"Generating Threads ~~ {secs:02d}s", end="\r")
        time.sleep(1)
        count_amt -= 1 

# Check acc type
def isGC(bearer):
    if requests.get("https://api.minecraftservices.com/minecraft/profile/namechange",
                       headers={"Authorization": "bearer " + bearer}).status_code == 404:
        return True
    else:
        return False

# EP Requests
def req(acc):
    # With closes socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('api.minecraftservices.com', 443))
        context = ssl.create_default_context()
        ss = context.wrap_socket(
                s, server_hostname='api.minecraftservices.com')
        ss.send(bytes(f'{acc.get("payload")}\r\n\r\n', 'utf-8'))
    output.append((ss.recv(423), time.time()))

def thread_send(count, acctype):
    global t
    threads = [threading.Thread(target=req, args=(acctype,)) for _ in range(count)]
    for t in threads:
        t.start()

# On Success
def success_true(token_list):
    t.join()
    threads = threading.active_count() - 1
    while threads:
        threads = threading.active_count() - 1
        print(f"Waiting for {threads} thread(s) to finish...")
        time.sleep(0.5)  # Wait until threads terminate
    # Sort Times
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/icons/944338449140420690/eaf9e293982fe84b1bb5ff08f40a17f9.webp?size=1024')
    output.sort(key=lambda sorts: sorts[1])
    for outs in output:
        statusCode = outs[0].decode("utf-8")[9:12]
        print(f"Recv: {statusCode} @ {datetime.datetime.utcfromtimestamp(outs[1]).strftime('%S.%f')}")
        if statusCode.isnumeric() and int(statusCode) == 200:
            try:
                webhook.add_embed(embed)
                webhook.execute()
            except requests.exceptions.MissingSchema:
                print("No Webhook Url Specified")
            except requests.exceptions.ConnectionError:
                print("Failed to send webhook")
            for token in token_list:
                username = requests.get(
                    "https://api.minecraftservices.com/minecraft/profile",
                    headers={"Authorization": "Bearer " + token.get("bearer")},
                ).json()["name"]
                if username == target_name:
                    skin_change = requests.post(
                        "https://api.minecraftservices.com/minecraft/profile/skins",
                        json={
                            "variant": "classic",
                            "url": "https://i.imgur.com/8nuxlIk.png",
                        },
                        headers={"Authorization": "Bearer " + token.get("bearer")},
                    )
                    if skin_change.status_code == 200:
                        print(f"{Fore.MAGENTA}Successfully delivered Skin Change{Fore.RESET}")
                    else:
                        print(f"{Fore.LIGHTRED_EX}Failed to deliver Skin Change{Fore.RESET}")
                    print(f"{Fore.MAGENTA}Sniped {Fore.RESET}{target_name}")

# Check for Dups accs
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

# Start main
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
#declaration
offset = 0
while len(code) < 1:
    code = input("invalid format |)-> ").split()
pinger = auto_ping(5)

if len(code) < 2:
    # auto offset
    print(f"\nOffset not specified, received: {pinger}ms\n")
    tune_delay = input("Tune Delay (press enter if false) -> ")
    if len(tune_delay) < 1:
        offset = float(pinger) / 1000
    else:
        offset = float(tune_delay) / 1000
else:
    offset = float(code[1])
        
target_name = code[0]
try:
    droptime = (droptimeApi(target_name) - offset)
except TypeError:
    droptime = int(input(f"{target_name} UNIX Timestamp ~> "))

# Authentication Proccess
with open('accs.txt', 'r') as f:
    # Ignore Spaces in text file
    lines = list(filter(lambda i: i, list(map(lambda s: s.strip("\n"), f.readlines()))))

with open("accs.txt") as file:
    for line in file.read().splitlines():
        if not line.strip():
            continue
        splitter = line.split(":")
        try:
            email, password = (splitter[0], splitter[1])
        except IndexError:
            print(f"Please Provide your password for {splitter[0]}")
            pass
        try:
            #Microsoft & Gc auth
            if (msresp := msmcauth.login(email, password).access_token) and isGC(msresp):
                print(f"Authenticated {email} [GC]")
                accdata.append({"type": "gc", "reqamount": 2, "bearer": msresp,
                                "payload": f"POST /minecraft/profile HTTP/1.1\r\nHost: api.minecraftservices.com\r\nprofileName: {target_name}\r\nAuthorization: Bearer {msresp}"})
            else:
                if NameChange(msresp) is True:
                    accdata.append({"type": "ms", "reqamount": 4, "bearer": msresp,
                                    "payload": f"PUT /minecraft/profile/name/{target_name} HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer {msresp}"})
                    print(f"Authenticated {email} [MS]")
                else:
                    print(f"{email} cannot namechange")
        except:
            auth = requests.post("https://authserver.mojang.com/authenticate",
                                  json={"username": email, "password": password})
            try:
                HEADER_NC = {"Authorization": f"Bearer {auth.json()['accessToken']}"}
            except KeyError:
                pass
            if auth.status_code == 200 and len((auth.json())) != 0:
                if NameChange(auth.json()['accessToken']):
                    print(f"Authenticated {email} [MJ]")
                    accdata.append({"type": "ms", "reqamount": 4, "bearer": auth.json()['accessToken'],
                                    "payload": f"PUT /minecraft/profile/name/{target_name} HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer {auth.json()['accessToken']}"})
                else:
                    print(f"{email} Cannot NameChange")
            else:
                print(f"Failed to authenticate {email}")

if not accdata:
    quit("No accounts Valid...")

# Webhook
webhook = DiscordWebhook(url=f'{WEBHOOK}', rate_limit_retry=True)
embed = DiscordEmbed(title="NameMC", url=f'https://namemc.com/search?q={target_name}',
                     description=f"**Sniped `{target_name}` :ok_hand:**", color=12282401)
# Prepare Sleep
try:
    countdown_time((droptime - time.time()) - 8)
except ValueError:
    pass
time.sleep(droptime - time.time())
for acc_data in accdata:
    thread_send(acc_data.get("reqamount"), acc_data)

success_true(accdata)
