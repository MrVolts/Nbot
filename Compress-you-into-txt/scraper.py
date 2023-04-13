import os
import json
default_save_path="../sourcesnbot/"
CATERGORYS = "abcdefghijklmnopqrstuvwxyz#"
matching_lines = []
all_messages = []
#list the files in default_save_path/GUILDNO

try:
    #open a file that has a dictionary of all the channels and the last line number read and store as dict
    with open("last_lines.json", "r") as f:
        last_lines = json.loads(f.read())
        
except FileNotFoundError:
    print("last_lines.json not found")
    last_lines = {}

try:
    #open a file that has a dictionary of all the channels and the last line number read and store as dict
    with open("usernames.json", "r") as f:
        usernames = json.loads(f.read())
        
except FileNotFoundError:
    print("usernames.json not found")
    usernames = {}

    

def discover_files(default_save_path,last_read_line):
    all_messages = []
    for file in os.listdir(f"{default_save_path}channels"):
        print(f"reading {file}...")
        
        #if the file is a json file
        if file.endswith(".jsonl"):
            if file not in dict.keys(last_read_line):
                last_read_line[file] = 0
            lineno = last_read_line[file]
            #open the file
            with open(f"{default_save_path}channels/{file}", "r") as f:
                #read the file into a list of lines
                lines = f.readlines()
            all_messages.extend(lines[lineno:])
            last_read_line[file] = len(lines)
    #save the last read line
    with open("last_lines.json", "w") as f:
        f.write(json.dumps(last_read_line))
    return all_messages

def get_ids(all_messages):
    #get all the ids
    ids = []
    names = []
    no_messages = []
    for line in all_messages:
        #load the line as json
        data = json.loads(line)
        #get the id
        if data["author_id"] not in ids:
            ids.append(data["author_id"])
            names.append(data["author_name"])
            no_messages.append(1)
        else:
            no_messages[ids.index(data["author_id"])] += 1
    return ids,names,no_messages

def create_folders():
    #create a number of folders depending on number of messages sent per user, and save the messages in the folder
    if not os.path.exists(f"{default_save_path}users"):
        os.makedirs(f"{default_save_path}users")

def save_user_messages(ids,names,no_messages,all_messages,usernames):
    for i in range(len(ids)):
        if ids[i] not in usernames:
            usernames[ids[i]] = names[i]
        if "/" in usernames[ids[i]]:
            usernames[ids[i]] = usernames[ids[i]].replace("/","-")
        for cat in CATERGORYS:
            if cat == usernames[ids[i]][0].lower() or cat == "#":
                if not os.path.exists(f"{default_save_path}users/{cat}"):
                    os.makedirs(f"{default_save_path}users/{cat}")
                with open(f"{default_save_path}users/{usernames[ids[i]]}|{str(ids[i])[0:3]}.jsonl", "a") as f:
                    for line in all_messages:
                        data = json.loads(line)
                        if data["author_id"] == ids[i]:
                            f.write(json.dumps(data)+"\n")
                break
    with open("usernames.json", "w") as f:
        f.write(json.dumps(usernames))

        
    

m = discover_files(default_save_path,last_lines)
print(f"found {len(m)} messages")
ids,names,messages = get_ids(m)
print("found {} users".format(len(ids)))
create_folders()
save_user_messages(ids,names,messages,m,usernames)
print("done")
