import json
import os
import requests

def index_json(obj):
    with open('../search_data/metadata.json') as f:
        metadata = json.load(f)

    paper_obj = {}
    metadata_obj = {}
    metadata_obj['paper_id'] = len(metadata)
    metadata_obj['authors'] = []
    for author_obj in obj['authors']:
        metadata_obj['authors'].append(author_obj['name'])
    metadata_obj['published_on'] = 1517443200
    metadata_obj['title'] = obj['title']
    metadata_obj['summary'] = obj['abstractText']
    metadata_obj['web_link'] = obj['url']
    metadata_obj['download_link'] = obj['url']

    text = metadata_obj["title"] + "."
    text += metadata_obj["summary"]
    paper_obj['title'] = metadata_obj["title"].lower()
    paper_obj['id'] = paper_obj['title']
    paper_obj['authors'] = [x.lower() for x in metadata_obj["authors"]]
    paper_obj['paper_number'] = metadata_obj['paper_id']

    num_sections = len(obj["sections"])
    for i in range(num_sections):
        text += obj["sections"][i]["text"]

    paper_obj['text'] = text.lower()

    metadata.append(metadata_obj)
    with open('../search_data/metadata.json', 'w') as f:
        json.dump(metadata, f)
        print("Metadata Updated")

    with open('../search_data/indexed_folder/'+str(metadata_obj['paper_id'])+'.json', 'w') as f:
        json.dump(paper_obj, f)
        print("JSON Processed and Saved")

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('http://localhost:8983/solr/project/update/json/docs', headers=headers, data=json.dumps(paper_obj))
    print(response.status_code)
    print("Paper Indexed")
