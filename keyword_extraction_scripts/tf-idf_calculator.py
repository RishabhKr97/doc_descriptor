import json
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

directory = os.fsencode('../data/')
all_files = [file.decode('ascii') for file in os.listdir(directory)]
error_logs = open('../data/keywords_extractor_error_logs.txt', 'a+')
error_logs.write("\n\n\n********** NEW LOGS **********\n")
with open('../data/metadata.json') as f:
    metadata = json.load(f)

index = 0
error_papers = 0
corpus = []

while True:
    if str(index)+'.json' not in all_files or index >= len(metadata):
        break

    with open('../data/'+str(index)+'.json') as f:
        curr_paper = json.load(f)

    text = metadata[index]["title"] + "."
    text += metadata[index]["summary"]

    if curr_paper["id"] == "empty" or "sections" not in curr_paper:
        error_logs.write(str(index)+"\n")
        error_papers += 1
    else:
        num_sections = len(curr_paper["sections"])
        if num_sections >= 1:
            text +=  curr_paper["sections"][0]["text"]
        if num_sections >= 2:
            text +=  curr_paper["sections"][1]["text"]
        if num_sections >= 3:
            text +=  curr_paper["sections"][-1]["text"]

        corpus.append(text)
    index += 1

error_logs.close()
print("Extracted corpus of {} papers with {} errors. Length of corpus = {}".format(index, error_papers, len(corpus)))
with open("../data/corpus", "wb") as fp:
    pickle.dump(corpus, fp)
print("Saved Documents Array")
# with open("test.txt", "rb") as fp:   # Unpickling
#     corpus = pickle.load(fp)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print(len(vectorizer.get_feature_names()))
print(X.shape)
print(vectorizer.get_stop_words())

import numpy as np
topn_ids = np.argsort(X[0])[::-1][:20]
print(len(topn_ids))
# for i in topn_ids:
#     print(vectorizer.get_feature_names()[i], X[0][i])