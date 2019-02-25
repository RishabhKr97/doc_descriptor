import json
import os
import requests

directory = os.fsencode('../data/')
headers = {
    'Content-type': 'application/pdf',
}

index = 0
all_files = [file.decode('ascii') for file in os.listdir(directory)]
error_logs = open('../data/json_conversion_error_logs.txt', 'a+')
error_logs.write("\n\n\n********** NEW LOGS **********\n")

while True:
    curr_paper = str(index)
    if curr_paper+".pdf" not in all_files:
        break

    if curr_paper+".json" in all_files:
        print("JSON for paper "+curr_paper+" already exists.")
    else:
        try:
            data = open('../data/'+curr_paper+'.pdf', 'rb').read()
            response = requests.post('http://scienceparse.allenai.org/v1', headers=headers, data=data)
            if response.status_code == 200:
                with open('../data/'+curr_paper+'.json', 'w') as f:
                    json.dump(response.json(), f)
                print(curr_paper+" converted to JSON.")
            else:
                print("Error code {} occured for paper {}".format(response.status_code, curr_paper))
                error_logs.write("Error code {} occured for paper {}\n".format(response.status_code, curr_paper))

        except Exception as e:
            print("Exception {} occured for paper {}.".format(e, curr_paper))
            error_logs.write("Exception {} occured for paper {}.".format(e, curr_paper))

        except:
            error_logs.close()
            raise

    index += 1

error_logs.close()