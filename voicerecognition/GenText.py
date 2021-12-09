import speech_recognition as sr

def getTextwithAudio(File):
    r = sr.Recognizer()

    with sr.AudioFile(File) as source:
        audio = r.record(source)

    text = r.recognize_google(audio,language='ja-JP')

    return text