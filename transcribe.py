import google.cloud.texttospeech as tts
import os
from flask import Flask, request, jsonify
import json
from google.cloud import speech 
from google.cloud import translate_v2 as translate
import six
import speech_recognition as sr
from scipy.signal import find_peaks, decimate
import scipy.io.wavfile as wavf
import wave
import numpy as np
import struct
import resampy
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import pymongo

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keys/client_service_key.json'
speech_client = speech.SpeechClient()

client = pymongo.MongoClient('TOKEN', server_api=ServerApi('1'))
db = client["Languages"]
collection = db.get_collection("Google Cloud Languages")


# file size needs to be < 10mbs and the length < 1 min
audioFile = ""

# translate variables
trans_client = translate.Client()
translate_lang = ""
text = ""

r = sr.Recognizer()
# translate the text
def transText(text, translate_lang):
    # change the text type to be put into the .translate function from the translate client
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
        
    translated = trans_client.translate(text, target_language=translate_lang)
    
    # print(translated)
    return translated["translatedText"]

# set audio files
def setAudioFile(audioF):
    audioFile = audioF
    return audioFile

# transcribe audio files
def openAudioFile(audioF):
    # rb is read binary
    with open(audioF, 'rb') as audio1:
        byte_audioFile = audio1.read()
    
    audioFile = speech.RecognitionAudio(content=byte_audioFile)
    return audioFile

# configure audio file, here we can set language
def configAudioFile(audioF, lang):
    configAudio = speech.RecognitionConfig(
    enable_automatic_punctuation = True,
    language_code = lang,
    audio_channel_count = 2
    )
    return configAudio    

#  transcribe config audio file
def transConfigAudio(configAudio, audioFile):
    transConfig = speech_client.recognize(
        config = configAudio,
        audio = audioFile
    )
    return transConfig


def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

app = Flask(__name__)

# generic route
@app.route('/', methods=['GET'])
def helloWorld():
    if request.method == "GET":
        # return jsonify({"a'": 1, 2:3})
        # return request.data
        return "Hello World"


# route 1 avail spoken lang
@app.route('/spoken', methods=['GET'])
def getSpokenLang():
    if request.method == "GET":
        stuff = collection.find({})
        arr = []
        for key in stuff:
            arr.append(key)
        return arr
    
# route 2 avail spoken lang
@app.route('/text', methods=['GET'])
def getTextLang():
    if request.method == "GET":
        stuff = collection.find({})
        arr = []
        for key in stuff:
            arr.append(key)
        return arr
    
# route 2 avail spoken lang
@app.route('/Update', methods=['POST'])
def Update():
    if request.method == "POST":
        updateCol = db["Options"]
        
        lang_from = {"language": lang_from }
        lang_to = {"text": lang_to}
        updateCol.update_one(lang_from, lang_to)
        
        

# route to parse data
@app.route('/caption', methods=['POST'])

def captionRoute():
    if request.method == "POST":
        # test()
        # print(request.json)
        # jsonData = request.json['sound']
        # print(jsonData)
        # print("Request \n")
        
        # print(request.data)
        
        # # print("JsonData")
        # jsonData = json.loads(request.data)
        
        # # print(type(jsonData))
        
        # # for key in jsonData:
        # #     print(key)
        # # print(jsonData["sound:"])
        # # real = ast.literal_eval(jsonData)
        # # print(real)

        # # print(data)
        # audio_file = getFromDylan(jsonData["sound:"])
        
        audio_file = "/home/ctran59/Caption-Software/test_audio/Welcome to Emma Saying!.wav"
        
        lang_from = "en-US"
        lang_to = lang_from
        text = ""
        transl8 = False
        
        # setting the audio stuff
        audioFile = setAudioFile(audio_file)
        audioFile = openAudioFile(audioFile)
        transFile = configAudioFile(audioFile, lang_from)
        transFile = transConfigAudio(transFile, audioFile)
        
        # checl if the language from and the language to is the same if not then we can set it true
        if (lang_from != lang_to):
            transl8 = True
            
        # setting the text
        for word in transFile.results:
            text += word.alternatives[0].transcript
        
        # if the translate feature is on, translate it and return it 
        if (transl8):
            trText = transText(text, lang_to)
            return trText
        
        return text
        # getFromDatabase()
        # jsonify()
        # return captionPost()
        return "Hello! We Are Here"

    
# parse the microphone raw data, raw_audio is an array full of integers
def getFromDylan(raw_audio):
    # open a wave file 
    # wav_file = ("audio.wav", "w")
    # wav_file.open()
    
    # amplitude = np.max(raw_audio) - np.min(raw_audio)
    # raw_audio = raw_audio * amplitude
    
    # raw_audio = np.array(raw_audio, dtype=np.int16)
    
    # factor = 2
    # raw_audio = decimate(raw_audio, factor)
    # raw_audio = raw_audio.tobytes()
    
    # raw_audio = np.frombuffer(raw_audio, dtype=np.int16)
    # raw_audio = raw_audio / 2**15
    # digital_signal = np.round(raw_audio * (2**15 - 1)).astype(np.int16)
    
    # with wave.open('digital_signal.wav', 'wb') as wavfile:
    #     wavfile.setnchannels(2)
    #     wavfile.setsampwidth(2)
    #     wavfile.setframerate(8000)
    #     wavfile.writeframes(digital_signal.tobytes()) 
        
    # Define the sampling rate and bit depth
    sample_rate = 44100
    bit_depth = 16

    # Define the desired number of samples, which can be calculated using numSamples = duration * sample_rate
    # hardcode the duration to be in seconds
    duration = 5

    # estimate the sample rate of the input
    current_sample_rate = len(raw_audio) / duration
    print("Current sample rate: " + str(current_sample_rate))
    
    # resample the data
    downsampled_data = resampy.resample(np.array(raw_audio), current_sample_rate, sample_rate)
    
    # normalize it
    normalized_data = (downsampled_data / np.max(downsampled_data)) * (2**15 - 1)
    resampled_data = normalized_data
    
    # Write the data to a .wav file
    with wave.open('output.wav', 'wb') as f:
        # Set the sample width (in bytes)
        sample_width = 2
        
        # Set the number of channels
        n_channels = 1
        
        # Set the number of samples
        n_samples = resampled_data.shape[0]
        
        # Set the parameters for the .wav file
        f.setsampwidth(sample_width)
        f.setnchannels(n_channels)
        f.setframerate(sample_rate)
        
        # Write the data to the .wav file
        f.writeframes(np.array(resampled_data, dtype=np.int16).tobytes())
    
    wav = sr.AudioFile('output.wav')
    with wav as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    
    r.recognize_google(audio, show_all = True)
    
    return wavfile

def getFromDataBase(lang_one, lang_two):
    # 
    # requests.get_json()
    lang_from = lang_one
    lang_to = lang_two
    return lang_one, lang_two

def jsonifyNeededData(wav_file, lang_to, lang_from):
    # puts the .wav the lang to and the language from into a jsonFile, nevermind just write it as a string its python lol
     # data = {'audio_file' : 'text_audiofile.wav', 
        #         'lang-from' : 'en-US', 
        #         'lang-to' : 'vi-VN',
        #         }
    jsonData = { 'audio_file' : wav_file, 
                'lang_to' : lang_to, 
                'lang_from' : lang_from }
    
    return jsonData
        
# parse the json data 
def captionPost(jsonData):        
        # getting json data from request and parsing it
        data = jsonData
        
        # initialized var to hold data
        audio_file = None
        lang_from = None
        lang_to = None
        
        if data:
            if 'audio_file' in data:
                audio_file = data['audio_file']
            if 'lang_from' in data:
                lang_from = data['lang_from']
            if 'lang_to' in data:
                lang_to = data['lang_to']
        
        # setting variables to hold text
        text = ""
        trText = ""
        transl8 = False
        
        # setting the audio stuff
        audioFile = setAudioFile(audio_file)
        audioFile = openAudioFile(audioFile)
        transFile = configAudioFile(audioFile, lang_from)
        transFile = transConfigAudio(transFile, audioFile)
        
        # checl if the language from and the language to is the same if not then we can set it true
        if (lang_from != lang_to):
            transl8 = True
            
        # setting the text
        for word in transFile.results:
            text += word.alternatives[0].transcript
        
        # if the translate feature is on, translate it and return it 
        if (transl8):
            trText = transText(text, lang_to)
            return trText
        
        return text
        
def test():
    # list_languages()
    english = 'en-US'
    audioFile = setAudioFile("/home/ctran59/Caption-Software/test_audio/Welcome to Emma Saying!.wav")
    audioFile = openAudioFile(audioFile)
    transFile = configAudioFile(audioFile, english)
    transFile = transConfigAudio(transFile, audioFile)
    # print(transFile)
    text = ""
    trText = ""
    for word in transFile.results:
        text += word.alternatives[0].transcript
        # print(word.alternatives[0].transcript)
    
    print("Original Text:\n")
    print(text)
    
    target = "vi-VN"
    trText = transText(text, "vi-VN")
    
    print("\nTranslated Text:\n")
    print(trText)
    

if __name__ == "__main__":
    # test()
    app.run(debug=True, port=10000, host='0.0.0.0')
    