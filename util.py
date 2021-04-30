import os
from dotenv import load_dotenv
import requests
import sounddevice as sd
from scipy.io.wavfile import write
import wave


def get_url(API_TOKEN, file):
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers={'authorization': API_TOKEN},
                             data=file)
    url = response.json()['upload_url']
    print('File Uploaded and got the url of the sample')
    return url


def get_id(API_TOKEN, url):
    response = requests.post('https://api.assemblyai.com/v2/transcript',
                             headers={
                                 "authorization": API_TOKEN,
                                 "content-type": "application/json"
                             },
                             json={
                                 "audio_url": url
                             })
    id = response.json()
    print('Got ID')
    return id['id']


def get_status(API_TOKEN, transcribe_id):
    response = requests.get(f'https://api.assemblyai.com/v2/transcript/{transcribe_id}',
                            headers={
                                "authorization": API_TOKEN,
                            })
    return response.json()


def upload_sample(sample):
    load_dotenv()
    API_TOKEN = os.getenv("API_TOKEN")
    url = get_url(API_TOKEN, sample)
    transcribe_id = get_id(API_TOKEN, url)
    return API_TOKEN, transcribe_id


# def record_sound(name, duration, freq=44100):
#     recording = sd.rec(int(duration * freq),
#                        samplerate=freq, channels=2)
#     sd.wait()
#     write(f"{name}.wav", freq, recording)
#     sound = open(f"{name}.wav")
#     return sound
