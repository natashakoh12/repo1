from flask import Flask, request, jsonify
from transformers import pipeline
import os
import tempfile
import subprocess
import json
import requests

app = Flask(__name__) #create flask application

#Initialize the ASR pipeline with wav2vec2-large-960h model
asr_pipeline = pipeline(task="automatic-speech-recognition", model="facebook/wav2vec2-large-960h")

#API endpoint to handle ASR requests
@app.route('/asr', methods=['POST'])
def asr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    
    #Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name +".mp3"
        file.save(file_path)

        
    try:
        #Perform ASR using the pipeline
        result = asr_pipeline(file_path)
        '''
        url = 'http://localhost:8001/asr'
        data = {
            'transcription': result,
            'additional_info': 'any_additional_data_you_want_to_send'
        }

        response = requests.post(url, json=data)

        print(response.json())
        '''
        transcription = result['text']
        
        
        #Get duration of the audio file
        duration = get_duration(file_path)
        
        response = {
            "transcription": transcription,
            "duration": duration
            }
        print(response)
        return transcription
    
    

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        #Clean up/delete temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            return ("temp file deleted")
        
#Fn to get audio duration (using ffmpeg)
def get_duration(file_path):
    command = ['ffmpeg', '-i', file_path, '-f', 'null', '-']  #no output will be written to disk
    result = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8') #run ffmpeg command and capture output
    duration = result.split('Duration: ')[1].split(', ')[0] #extract duration from ffmpeg output
    return duration


if __name__ == '__main__':
    app.run(host='localhost', port=8001, debug=True)