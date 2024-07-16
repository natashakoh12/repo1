import os
import csv
import requests
from flask import Flask, request, jsonify
from asr_api import asr

# Define your ASR API endpoint
ASR_API_URL = 'http://localhost:8001/asr' 
app = Flask(__name__)

# Example route to handle GET requests
@app.route('/asr', methods=['GET'])


#Fn to iterate through each mp3 file in the folder and push it to ASR API
def transcribe_audio_files(folder_path):
    results = []
    
    for filename in os.listdir(folder_path): #Iterate through each file in the folder
        if filename.endswith('.mp3'):
            file_path = os.path.join(folder_path, filename)
            
            files = {'file': open(file_path, 'rb')} #Prepare data to send to ASR API
            
            try:
                response = requests.post(ASR_API_URL, files=files) #Make POST request to ASR API
                print(response)
                
                if response.status_code == 200: #Check if the request was successful
                    print(response.text)
     
                    try:
                        # Try to parse JSON response 
                        #results_from_asr_api = asr()
                        #print(results_from_asr_api)
                        '''
                        if results_from_asr_api: 
                            print(results_from_asr_api)
                            transcription = results_from_asr_api[0]
                            print("transcription:", transcription)
                            '''
                        generated = response.json()['text']
                        transcription = generated['transcription']
                        print(transcription)
                        results.append({'filename': filename, 'generated_text': transcription})
                    except (KeyError, ValueError) as e:
                        print(f"Error parsing JSON response for {filename}: {e}")
                else:
                    print(f"Error processing {filename}: Status code {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"Request to ASR API failed for {filename}: {e}")
    
    return results

def fetch_data_from_api(folder_path):
    for filename in os.listdir(folder_path): #Iterate through each file in the folder
        if filename.endswith('.mp3'):
            file_path = os.path.join(folder_path, filename)
            
            files = {'file': open(file_path, 'rb')} #Prepare data to send to ASR API
            
            response = requests.post(ASR_API_URL, files=files) #Make POST request to ASR API
            print(response)
                
            if response.status_code == 200: #Check if the request was successful
                try:
                    response = requests.get(ASR_API_URL)
                    if response.status_code == 200:
                        data = response.json()  # Parse JSON response into Python dictionary
                        return data
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Request to API failed: {e}")
                    return None

# call above fn, update CVS file with results and save it back to folder
def main():
    # Path to the folder containing MP3 files
    folder_path = "C:/Users/65973/source/repos/repo1/asr/cv-valid-dev" 
    
    # Transcribe audio files
    results = (transcribe_audio_files(folder_path))
    #results = fetch_data_from_api(folder_path)
    
    # Update CSV file with generated_text column
    csv_file = os.path.join(folder_path, 'cv-valid-dev.csv') #assume existing csv file in the designated folder
    update_csv(csv_file, results)
    
    print("Transcription process completed.")

def update_csv(csv_file, results):
    # Read the existing CSV file and add generated_text column
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['generated_text']
        rows = list(reader)
    
    # Update rows with generated_text
    for row in rows:
        for result in results:
            if row['filename'] == result['filename']:
                row['generated_text'] = result['generated_text']
                break
    
    # Write updated rows back to the CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
    app.run(debug=True)

