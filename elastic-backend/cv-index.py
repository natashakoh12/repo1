
#this script will read data from cs-valid-dev.csv and index it into Elasticsearch.
#please ensure "cs-valid-dev.csv" file is in the same directory

import csv
import pandas as pd
from elasticsearch import Elasticsearch, helpers

# Elasticsearch connection
es = Elasticsearch(['http://localhost:9200']) #establish a connection to elasticsearch running on 9200



index_name = 'cv-transcriptions' #Define the index name

if not es.indices.exists(index=index_name): #Create the index if it doesn't exist
    es.indices.create(index=index_name)
#Fn to clean csv
def clean_data(row):
    #print("cleaning")
    cleaned_row = {}
    for key, value in row.items():
        if isinstance(value, str):
            cleaned_row[key] = value.replace("'", "") #cleaning apostrophe
        else:
            cleaned_row[key] = value
    return cleaned_row

#Fn to generate documents from CSV
def generate_documents(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for raw_row in reader:
            row = clean_data(raw_row)
            yield {
                "_index": index_name,
                "_source": {
                    "generated_text": row.get("generated_text"),
                    "duration": row.get("duration"),
                    "age": row.get("age"),
                    "gender": row.get("gender"),
                    "accent": row.get("accent")
                }
            }

#Index documents from CSV
csv_file = 'cv-valid-dev.csv'
helpers.bulk(es, generate_documents(csv_file))

print(f"Data indexed into Elasticsearch index '{index_name}' successfully.")

#Execute the script to index the data into Elasticsearch
  