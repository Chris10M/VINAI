import speech_recognition as sr
import threading
from pygame import mixer


class SpeechTags:
    CANNOT_UNDERSTAND_AUDIO = 'CANNOT UNDERSTAND AUDIO'
    CAPTURE_PHRASE = 'vinay'
    beep_path = 'beep.mp3'

    mixer.init()
    mixer.music.load(beep_path)



class Speech(threading.Thread):
# Record Audio
    def __init__(self):
        threading.Thread.__init__(self)
        self.r = sr.Recognizer()
        self.r.energy_threshold = 4000
        self.r.pause_threshold = 0.8
        self.key = 'AIzaSyB2CSAWgtuNoV3sQLLJcdwG_rGTwym6ReQ'
        self.phrase = ''

    def run(self):
        while True:
            with sr.Microphone() as source:
                print('listening')
                audio = self.r.listen(source)
                print('end listening')
            # Speech recognition using Google Speech Recognition
            try:
                self.phrase = self.r.recognize_google(audio, key=self.key)
            except sr.UnknownValueError:
                self.phrase = SpeechTags.CANNOT_UNDERSTAND_AUDIO
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def get_phrase(self):
        if self.phrase is '':
            return None
        else:
            return self.phrase


class SpeechWorker:
    old_phrase = None
    flag = False
    speech_thread = Speech()
    speech_thread.start()

    @staticmethod
    def get():
        current_phrase = SpeechWorker.speech_thread.get_phrase()
        if current_phrase is None:
            pass
        else:
            if SpeechWorker.old_phrase == current_phrase:
                pass
            else:
                SpeechWorker.old_phrase = current_phrase

                if current_phrase.lower() == SpeechTags.CAPTURE_PHRASE:
                    mixer.music.play()
                    print('vinay')
                    SpeechWorker.flag = True
                    return None

                if SpeechWorker.flag is True:
                    SpeechWorker.flag = False
                    return current_phrase

        return None

    @staticmethod
    def get_without_capture():
        current_phrase = SpeechWorker.speech_thread.get_phrase()
        if current_phrase is None:
            pass
        else:
            if SpeechWorker.old_phrase == current_phrase:
                pass
            else:
                SpeechWorker.old_phrase = current_phrase
                return current_phrase

        return None




if __name__ == '__main__':
    speech_thread = Speech()

    speech_thread.start()

    import time

    while True:
        print(speech_thread.get_phrase())
        #time.sleep(1)

    speech_thread.join()