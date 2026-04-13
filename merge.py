import json
import os
from glob import glob

os.makedirs("output", exist_ok=True)

active = []
noactive = []
banned = []
not_found = []

files = glob("artifacts/**/*.json", recursive=True)

for file in files:
    with open(file, "r") as f:
        data = json.load(f)

        if "active_" in file:
            active.extend(data)

        elif "noactive_" in file:
            noactive.extend(data)

        elif "banned_" in file:
            banned.extend(data)

        elif "not_found_" in file:
            not_found.extend(data)

# sortowanie
active.sort(key=lambda x: x["id"])
noactive.sort(key=lambda x: x["id"])
banned.sort(key=lambda x: x["id"])
not_found.sort(key=lambda x: x["id"])

with open("output/active.json", "w") as f:
    json.dump(active, f, indent=2)

with open("output/noactive.json", "w") as f:
    json.dump(noactive, f, indent=2)

with open("output/banned.json", "w") as f:
    json.dump(banned, f, indent=2)

with open("output/not_found.json", "w") as f:
    json.dump(not_found, f, indent=2)

print("MERGE DONE")
