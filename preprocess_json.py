import requests
import os
import json
import numpy as np
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embedding(text_list):
    # https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings
    r = requests.post("http://localhost:11434/api/embed", json={
        "model" : "bge-m3",
        "input": text_list
    })

    embedding = r.json()['embeddings']
    return embedding

jsons = os.listdir("jsons") # List all the jsons
# print(jsons)
my_dict = []
chunk_id = 0

for json_file in jsons:  # Loop through each json file
    with open(f"jsons/{json_file}") as f: # Read content of each json file
        content = json.load(f)
    print(f"Creating Embeddings for {json_file}")    # status of the json files
    embeddings = create_embedding([c['text'] for c in content['chunks']]) # Create embed as a list of strings
        
    for i, chunk in enumerate(content['chunks']): # iterate all the chunks
        chunk['chunk_id'] = chunk_id # add chunk_id
        chunk['embedding'] = embeddings[i] # add embeddings
        chunk_id += 1
        my_dict.append(chunk)
       # if(i == 3): # Read 5 chunks for now
       #     break
    # break    
    # break 
# print(my_dict)

df = pd.DataFrame.from_records(my_dict)
# save this dataframe 
joblib.dump(df, 'embeddings.joblib')
# print(df)
