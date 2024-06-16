import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv
import wave
import sys
import pyaudio
import audioop
from scipy.io import wavfile


import math
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



from gpiozero import CPUTemperature
from time import sleep, strftime, time


urlThingsBoard = 'http://DESKTOP-KD82ADA.local:8088/api/v1/1bpxua4miiqab1i5px2e/telemetry'
score = 0
cpuTemperature = 0
soundPresuredB = 0
classDetected = 'Silent'
classId = 0

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

touched = False
touchedKey = 0
touchData = 0


# Find the name of the class with the top score when mean-aggregated across frames.
def class_names_from_csv(class_map_csv_text):
  """Returns list of class names corresponding to score vector."""
  class_names = []
  with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      class_names.append(row['display_name'])

  return class_names



def ensure_sample_rate(original_sample_rate, waveform,
                       desired_sample_rate=16000):
  """Resample waveform if required."""
  if original_sample_rate != desired_sample_rate:
    desired_length = int(round(float(len(waveform)) /
                               original_sample_rate * desired_sample_rate))
    waveform = scipy.signal.resample(waveform, desired_length)
  return desired_sample_rate, waveform

def process_file(wav_file_name, maximum) :
    global classDetected, score, classId
    sample_rate, wav_data = wavfile.read(wav_file_name, 'rb')
    # sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)
    
    # Show some basic information about the audio.
    duration = len(wav_data)/sample_rate
    print(f'Sample rate: {sample_rate} Hz')
    print(f'Total duration: {duration:.2f}s')
    print(f'Size of the input: {len(wav_data)}')
    
    # Listening to the wav file.
    # Audio(wav_data, rate=sample_rate)
    
    # The wav_data needs to be normalized to values in [-1.0, 1.0]
    waveform = wav_data / tf.int16.max
    
    # Run the model, check the output.
    scores, embeddings, spectrogram = model(waveform)
    
    scores_np = scores.numpy()
    #spectrogram_np = spectrogram.numpy()
    classId = scores_np.mean(axis=0).argmax()
    infered_class = class_names[classId]

    print(f'The main sound is: {infered_class}')
    classDetected = infered_class
    score = round(scores_np.mean(axis=0).max()*100.0,2)

    


    

def showLevel(level):
    buffer = [0]*20
    if (level > 99):
        level = 99
    if (level <0 ):
        level = 0
    j = 0
    for j in range (int(level / 5)) :
        buffer[j] = 5
    if (j % 5) > 0:
        buffer[int(level/5)] = level % 5
    for k in range (int(level / 5) + 1, 20) :
        buffer[k] = 0
        

    

    
  


# Init pyAudio    
p = pyaudio.PyAudio()
# Temperature sensor setup
cpu = CPUTemperature()

print("Loading model")  

# Load the model.
# model = hub.load('https://tfhub.dev/google/yamnet/1')
model = hub.load('./yamnet_model')

class_map_path = model.class_map_path().numpy()
class_names = class_names_from_csv(class_map_path)

print("Processing")    

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 1



try:
    while True:
        temp = cpu.temperature
        cpuTemperature = temp
        
        if touched:
            
            for i in range(12):
                if (touchData & (1<<i)):
                    touchedKey = i
                    print("Kbd touched {}".format(i))
                    #break
            touched = False
        
        
        maximum = 0
        
        with wave.open('yamnet.wav', 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

            print('Recording...')

            for _ in range(0, int(RATE // CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                wf.writeframes(data)
               
                db = 20 * math.log10(audioop.rms(data, 2))
                if db > maximum :
                    maximum = db

                showLevel(int(db)-40)

            print('Done')
            
            
        stream.close()  
        soundPresuredB = maximum
        print('Processing...')

        process_file('yamnet.wav', maximum)
        jsonDataValues = {'temperature':cpuTemperature,'db':soundPresuredB,'score':score,'class':classDetected,'latitude':41.65658725063826,'longitude':-0.8789170307124832,'classId':int(classId)}
        try:
            r = session.post(urlThingsBoard, json = jsonDataValues, timeout=(2, 10))
        except Exception as e: 
            print(e)
except Exception as e: 
    print(e)

    p.terminate()
else:
    p.terminate()






