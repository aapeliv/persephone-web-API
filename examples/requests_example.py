"""
This file shows how you can interact with the Persephone API with the requests library.
See http://docs.python-requests.org/en/master/ for requests library documentation.
"""
import os
import requests

API_VERSION  = "v0.1"
# Where the API is being served from
URL_BASE = "http://127.0.0.1:8080/{}/".format(API_VERSION)

EXAMPLE_FILES_DIR = "example_files"

# upload an audio file
files = {'audioFile': open(os.path.join(EXAMPLE_FILES_DIR, 'crdo-NRU_F4_ACCOMP_PFV.1.wav'), 'rb')}

audio_url = URL_BASE + "audio"
r = requests.post(audio_url, files=files)

print(r.text)
audio_results = r.json()
audio_id = audio_results['id']
print("File uploaded has an id of {}".format(audio_id))


# upload a transcription
files = {'transcriptionFile': open(os.path.join(EXAMPLE_FILES_DIR, 'crdo-NRU_F4_ACCOMP_PFV.1.phonemes'), 'rb')}

transcription_url = URL_BASE + "transcription"
r = requests.post(transcription_url, files=files)
print(r.text)
transcription_results = r.json()
transcription_id = transcription_results['id']
print("transcription uploaded has an id of {}".format(transcription_id))


# Create an utterance from the audio file and transcription uploaded before

utterance_data = {
    "audioId": audio_id,
    "transcriptionId": transcription_id
}

utterance_url = URL_BASE + 'utterance'

# Note that this endpoint expects JSON data so we pass json
# instead of data to the request
r = requests.post(utterance_url, json=utterance_data)
print(r.text)
utterance_results = r.json()
utterance_id = utterance_results['id']
print("Utterance created on server has an id of {}".format(utterance_id))
