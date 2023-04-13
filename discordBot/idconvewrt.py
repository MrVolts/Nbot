import json
import os
#create a default save path in home/ubuntu
default_save_path = "/home/ubuntu/NomadsAI/sourcesnbot"
def convert_to_36(original):
    if original == 0:
        return "0"
    digits = []
    while original > 0:
        digits.append(original % 36)
        original = original // 36
    digits.reverse()
    for i in range(0,len(digits)):
        if digits[i] > 9:
            digits[i] = chr(digits[i] + 87)
    return "".join(str(x) for x in digits)
try:
    with open(f"{default_save_path}/iddqss.json", "r") as f:
            ids = json.loads(f.read())
except FileNotFoundError:
    print("ids.json not found")
    ids = {"#idnumber":0}
def convert_to_zid(original):
    global ids
    try:
        return ids[original]
    except KeyError:
        zid = convert_to_36(ids["#idnumber"])
        ids["#idnumber"] += 1
        ids[original] = zid
        with open(f"/{default_save_path}/iddqss.json", "w") as f:
            f.write(json.dumps(ids))
        pass
    return(zid)

def convert_to_discordid(original):
    return list(ids.keys())[list(ids.values()).index(original)]
def return_all():
    return ids
for i in range(0,10):
    print(convert_to_zid(str(i)))