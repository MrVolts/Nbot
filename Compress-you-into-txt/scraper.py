import os
import json
default_save_path="../sourcesnbot/"
GUILDNO = 711625884771287151
search_terms = ["596713937626595382"]#,"volts"]
file_name = "princess"
matching_lines = []
all_messages = []
#list the files in default_save_path/GUILDNO
for file in os.listdir(f"{default_save_path}{GUILDNO}"):
    print(f"reading {file}...")
    #if the file is a json file
    if file.endswith(".json"):
        #open the file
        with open(f"{default_save_path}{GUILDNO}/{file}", "r") as f:
            #read the file into a list of lines
            lines = f.readlines()
            all_messages.extend(lines)
print(len(all_messages),"messages found")
for message in all_messages:
    for term in search_terms:
        if term.lower() in str(eval(message)["author_id"]).lower():
            matching_lines.append(eval(message))
            break
print(len(matching_lines),"results found")

#w

print((((len(matching_lines)/len(all_messages))*10000000)//1000)/100,"% of messages match terms")

#save this to a file with the name being file_name
with open(f"{file_name}.json", "w") as f:
                    for item in matching_lines:
                        #write each item in the list to a new line
                        f.write(json.dumps(item)+"\n")
print("done")