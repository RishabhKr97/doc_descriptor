import json
import os

directory = os.fsencode('../search_data/indexed_folder_200/')
all_files = [file.decode('ascii') for file in os.listdir(directory)]

directory_context = os.fsencode('../search_data/contextManipulated/')
all_files_context = [file.decode('ascii') for file in os.listdir(directory_context)]

index = 0
error_papers = 0

while True:
    if index >= len(all_files):
        break
    if str(index)+'.json' not in all_files:
        index += 1
        continue

    with open('../search_data/indexed_folder/'+str(index)+'.json') as f:
        curr_paper = json.load(f)

    if str(index)+'.json' not in all_files_context:
        error_papers += 1
        index += 1
        print("Error in "+str(index)+'.json')
        continue

    with open('../search_data/contextManipulated/'+str(index)+'.json') as f:
        curr_context = json.load(f)

    if "C1" not in curr_context or "C2" not in curr_context or "C3" not in curr_context:
        error_papers += 1
        index += 1
        print("Error in "+str(index)+'.json')
        continue


    obj = {}
    obj['title'] = curr_paper['title']
    obj['authors'] = curr_paper['authors']
    obj['text'] = curr_paper['text']
    obj["C1"] = ""
    obj["C2"] = ""
    obj["C3"] = ""

    for key in curr_context["C1"].keys():
        obj["C1"] += " " + key
    for key in curr_context["C2"].keys():
        obj["C2"] += " " + key
    for key in curr_context["C3"].keys():
        obj["C3"] += " " + key


    with open('../search_data/context_indexed_folder_200/'+str(index)+'.json', 'w') as f:
        json.dump(obj, f)
    print(str(index)+'.json'+' processed successfully.')

    index += 1

print("TOTAL ERROR = {}".format(error_papers))
