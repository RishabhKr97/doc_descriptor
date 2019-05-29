from flask import Flask
from flask import request
from flask import Response
from index_data import index_json
from search_data import search_with_context
from search_data import search_without_context
import urllib.request
import requests
import json

app = Flask(__name__)

@app.route("/pdf_link/")
def parse_pdf():
    url = request.args.get('url')
    urllib.request.urlretrieve(url, 'temp_file.pdf')
    data = open('temp_file.pdf', 'rb').read()

    headers = {
    'Content-type': 'application/pdf',
    }
    response = requests.post('http://35.200.140.148:8080/v1', headers=headers, data=data)
    obj = response.json()
    if response.status_code == 200 and obj['id'] != "empty" and "sections" in obj:
        print("GOT Response 200")
        obj['url'] = url
        index_json(obj)
        print("New Paper Indexed.")
        return json.dumps({'success':True}), 201, {'ContentType':'application/json'}
    else:
        print("No Response")
        return Response(status=412)

@app.route("/search/")
def search_results():
    query = request.args.get('q')
    data = search_with_context(query)
    return json.dumps(data), 200, {'ContentType':'application/json'}

@app.route("/search_no_context/")
def search_no_context_results():
    query = request.args.get('q')
    data = search_without_context(query)
    return json.dumps(data), 200, {'ContentType':'application/json'}

app.run(debug=True)
