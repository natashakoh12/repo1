import os
import csv
import requests
from flask import Flask, request, jsonify
from asr_api import asr

# Define your ASR API endpoint
ASR_API_URL = 'http://localhost:8001/asr' 
app = Flask(__name__)
#curl -F 'file=@C:/Users/HTX CBRNE/PycharmProjects/NAT/flask

# Example route to handle GET requests
@app.route('/send_to_server', methods=['POST'])

#Fn to iterate through each mp3 file in the folder and push it to ASR API
def transcribe_audio_files(folder_path):
    csv_file = os.path.join(folder_path, 'cv-valid-dev.csv') #assume existing csv file in the designated folder
    initialise_csv(csv_file)

    for filename in os.listdir(folder_path): #Iterate through each file in the folder
        if filename.endswith('.mp3'):
            file_path = os.path.join(folder_path, filename)
            
            files = {'file': open(file_path, 'rb')} #Prepare data to send to ASR API
            
            try:
                response = requests.post(ASR_API_URL, files=files) #Make POST request to ASR API
                print(response)
                
                if response.status_code == 200: #Check if the request was successful
     
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
                        reply = requests.get(ASR_API_URL)
                        print(reply)
                        generated_text = reply.json()['transcription']
                        duration = reply.json()['duration']
                        results ={'generated_text': generated_text, 'duration': duration}
                        append_csv(csv_file,results)
                        print(results)
                    except (KeyError, ValueError) as e:
                        print(f"Error parsing JSON response for {filename}: {e}")
                else:
                    print(f"Error processing {filename}: Status code {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"Request to ASR API failed for {filename}: {e}")
    
    return results



# call above fn, update CVS file with results and save it back to folder
def main():
    # Path to the folder containing MP3 files
    folder_path = "C:/Users/65973/source/repos/repo1/asr/cv-valid-dev" 
    
    # Transcribe audio files
    results = (transcribe_audio_files(folder_path))
    
    
    print("Transcription process completed.")

def initialise_csv(csv_file):
    file = open(csv_file, "w")
    writer = csv.writer(file)
    file.truncate()
    writer.writerow(["generated_text","duration"])
    file.close()

def append_csv(csv_file, dict):
    with open(csv_file, 'a',newline="") as file:  
        writer = csv.writer(file)
        text = dict['generated_text']
        time = dict['duration']
        print(text,time)
        writer.writerow([text,time])
    file.close()


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
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerows(result)

if __name__ == "__main__":
    main()
    #app.run(debug=True) #to stop flask app from automatically starting again and wiped out my csv

