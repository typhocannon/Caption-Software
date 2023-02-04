import google.cloud.texttospeech as tts
import json
import os
from flask import Flask, requests, jsonify
from google.cloud import speech 
from google.cloud import translate_v2 as translate
import six

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/ctran59/Caption-Software/keys/client_service_key.json'
speech_client = speech.SpeechClient()

# file size needs to be < 10mbs and the length < 1 min
audioFile = ""

# translate variables
trans_client = translate.Client()
translate_lang = ""
text = ""

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
@app.route('/caption', methods=['POST'])

def captionRoute():
    if requests.method == "POST":
        return "Hello! We Are Here"
    # getFromDylan()
    # getFromDatabase()
    # jsonify()
    # return captionPost()
    
def getFromDylan(raw_audio):
    # parse the microphone
    wav = raw_audio
    return wav

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
    audioFile = setAudioFile("/home/ctran59/Caption-Software/test_audio/Sunday.wav")
    audioFile = openAudioFile(audioFile)
    transFile = configAudioFile(audioFile, 'vi-VN')
    transFile = transConfigAudio(transFile, audioFile)
    # print(transFile)
    text = ""
    trText = ""
    for word in transFile.results:
        text += word.alternatives[0].transcript
        # print(word.alternatives[0].transcript)
    
    print("Original Text:\n")
    print(text)
    
    target = "en-US"
    trText = transText(text, target)
    
    print("\nTranslated Text:\n")
    print(trText)
    

if __name__ == "__main__":
    test()
    app.run(debug=True, port=9090)
    