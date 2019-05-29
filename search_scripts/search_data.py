import requests
import json
import random

def search_with_context(q):
    params = (
        ('fl', '*,score'),
        ('q', q),
        ('rows', '20'),
    )
    response = requests.get('http://localhost:8983/solr/project/select', params=params)
    response = response.json()

    with open('../search_data/metadata.json') as f:
        metadata = json.load(f)

    docs = []
    # print(response)
    maxScore = response['response']['maxScore']+1
    for result in response['response']['docs']:
        # print(result)
        for data in metadata:
            # print(data)
            if data['paper_id'] == result['paper_number'][0]:
                obj = {}
                obj['title'] = data['title']
                obj['published_on'] = data['published_on']
                obj['authors'] = data['authors']
                obj['summary'] = data['summary']
                obj['download_link'] = data['download_link']
                obj['web_link'] = data['web_link']
                obj['score'] = '%.5f'%(result['score']/maxScore)
                docs.append(obj)
                break

    return docs


def search_without_context(q):
    params = (
        ('fl', '*,score'),
        ('q', q),
        ('rows', '20'),
    )
    response = requests.get('http://localhost:8983/solr/project/select', params=params)
    response = response.json()

    with open('../search_data/metadata.json') as f:
        metadata = json.load(f)

    docs = []
    # print(response)
    maxScore = response['response']['maxScore']+5
    part_one = response['response']['docs'][:5]
    part_two = response['response']['docs'][5:]
    random.shuffle(part_one)
    random.shuffle(part_two)
    part_one += part_two

    print("****",q)
    print(part_one)
    for result in part_one:
        # print(result)
        for data in metadata:
            # print(data)
            if data['paper_id'] == result['paper_number'][0]:
                obj = {}
                obj['title'] = data['title']
                obj['published_on'] = data['published_on']
                obj['authors'] = data['authors']
                obj['summary'] = data['summary']
                obj['download_link'] = data['download_link']
                obj['web_link'] = data['web_link']
                obj['score'] = '%.5f'%(result['score']/maxScore)
                docs.append(obj)
                break

    return docs