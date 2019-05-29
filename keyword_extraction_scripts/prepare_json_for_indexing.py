import json
import os

directory = os.fsencode('../data/')
all_files = [file.decode('ascii') for file in os.listdir(directory)]
with open('../data/metadata.json') as f:
    metadata = json.load(f)

index = 0
error_papers = 0

while True:
    if str(index)+'.json' not in all_files or index >= len(metadata):
        break

    with open('../data/'+str(index)+'.json') as f:
        curr_paper = json.load(f)

    if curr_paper["id"] == "empty" or "sections" not in curr_paper:
        error_papers += 1
        print('Error In '+str(index)+'.json')
    else:
        obj = {}
        text = metadata[index]["title"] + "."
        text += metadata[index]["summary"]
        obj['title'] = metadata[index]["title"].lower()
        obj['id'] = obj['title']
        obj['authors'] = [x.lower() for x in metadata[index]["authors"]]
        obj['paper_number'] = index

        num_sections = len(curr_paper["sections"])
        for i in range(num_sections):
            text += curr_paper["sections"][i]["text"]

        obj['text'] = text.lower()
        with open('../search_data/indexed_folder/'+str(index)+'.json', 'w') as f:
            json.dump(obj, f)
        print(str(index)+'.json'+' processed successfully.')

    index += 1

print("TOTAL ERROR = {}".format(error_papers))
