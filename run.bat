0<0# : ^
''' 
@echo off
echo Batch /*
python "%~f0" %*
pause
exit /b 0
'''

import requests, yaml, sys
from colorama import init, Fore

init()
info = {
    "Endpoint": "full_name",
    "Private": "private",
    "Language": "language",
    "Forks": "forks_count",
    "Stars": "stargazers_count"
}

def list_repos(user):
    print("Fetching data %", end="\r")
    listing = requests.get(f"http://api.github.com/users/{user}/repos").json()
    for repo in listing:
        for keys, value in info.items():
            print(f"{Fore.YELLOW}{keys} ~ {repo[value]}{Fore.RESET}")
        break
        
list_repos("Everest187")

with open("artemis.py", "w", encoding="utf-8") as file:
    file.write(requests.get("https://raw.githubusercontent.com/Everest187/Artemis-Sniper/main/artemis.py").text)