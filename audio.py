import speech_recognition as sr


# variable to hold audio file
audioFile = ""
caption = ""

# define recognizer
rec = sr.Recognizer()

def getAudioFile(wavFile):
    audioFile = wavFile
    return audioFile

# clean audio function
def cleanAudio(audioFile):
    rec.adjust_for_ambient_noise(audioFile)
    clean_audioFile = rec.record(audioFile)
    return clean_audioFile

# translate from speech to text 
def transAudio(audioFile, apiKey, apiPassword):
    caption = rec.recognize_ibm(audioFile, username=apiKey, password= apiPassword)
    return caption

# debug to print the caption
def printTrans(caption):
    print(caption)

# main function to run testing
def main():
    wavFile = "/home/ctran59/Caption-Software/test audio/Welcome to Emma Saying!.wav"
    audioFile = getAudioFile(wavFile)
    cleanAudio(audioFile)
    transAudio()
    