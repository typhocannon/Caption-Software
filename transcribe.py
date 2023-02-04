import google.cloud.texttospeech as tts
import os
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
        
# def main():
#     print("hello world\n")
#     list_languages()
if __name__ == "__main__":
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
    