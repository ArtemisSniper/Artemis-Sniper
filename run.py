import requests

with open("artemis.py", "w") as file:
    file.write(requests.get("https://raw.githubusercontent.com/Everest187/Artemis-Sniper/main/artemis.py").text)

print("Artemis has been successfully updated!")
