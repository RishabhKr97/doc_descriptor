import ast
import datetime
import json
import urllib.request

with open('../data/arxivData.json') as f:
    data = json.load(f)

try:
    with open('../data/metadata.json') as f:
        metadata = json.load(f)
except FileNotFoundError:
    metadata = []

if metadata:
    beg_index = metadata[-1]['paper_id']+1
else:
    beg_index = 0

def save_metadata():
    with open('../data/metadata.json', 'w') as f:
        json.dump(metadata, f)

try:
    for i in range(beg_index, len(data)):
        obj = {}
        obj['paper_id'] = i
        obj['authors'] = []
        for author in ast.literal_eval(data[i]['author']):
            obj['authors'].append(author['name'])
        obj['published_on'] = int(datetime.datetime(data[i]['year'], data[i]['month'], data[i]['day'], tzinfo=datetime.timezone.utc).timestamp())
        obj['title'] = data[i]['title']
        obj['summary'] = data[i]['summary']
        obj['tags'] = []
        for tag in ast.literal_eval(data[i]['tag']):
            term = tag['term'].rsplit('.',1)
            if len(term) > 1:
                obj['tags'].append(term[1])
        obj['web_link'] = ast.literal_eval(data[i]['link'])[0]['href']
        obj['download_link'] = ast.literal_eval(data[i]['link'])[1]['href']
        urllib.request.urlretrieve(obj['download_link'], '../data/'+str(obj['paper_id'])+'.pdf')

        metadata.append(obj)
        print("Paper "+str(obj['paper_id'])+" : '"+obj['title']+"' downloaded.")

        if i % 20 == 0:
            save_metadata()

    save_metadata()
except (KeyboardInterrupt, SystemExit):
    save_metadata()
