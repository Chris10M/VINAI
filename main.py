from chatbot import ChatBot
from speech_regonition import SpeechWorker
from ocr_reader import Ocr
from maps import Map

import pyttsx3
import time
import datetime


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")

    return current_time


class Say:
    speech_driver = 'espeak'
    engine = pyttsx3.init()

    @staticmethod
    def phrase(text):
        print(text)
        Say.engine.say(text)
        Say.engine.runAndWait()


class OcrObject:
    flag = False
    ocr_thread = None


class Responses:
    map_direction = 'where to you want to go?'
    map_current_location = 'get_current_location'
    ocr_on = 'ocr_on'
    stop_ocr = 'stop_ocr'
    scan_page = 'scan_page'
    get_nearest_bus_stop = 'get_nearest_bus_stop'
    current_time = 'current_time'
    name = 'My name is VINAI.'
    hello = 'Hello there Human.'
    not_understand = "I didn't understand. You can try rephrasing."
    say_ocr_mode_on = 'The OCR mode is on'
    say_scan_page = 'scanning page stay still'

    accurate = 0

    @staticmethod
    def bus_stop_name(stop_name):
        text = 'The nearest bus stop is ' + stop_name
        return text

    @staticmethod
    def directions_intent():
        text = 'The directions to get there is'
        time.sleep(1)

        return text

    @staticmethod
    def place_name(place):
        text = 'getting directions for the place ' + place
        return text


def response_select(response):
    if response == Responses.map_direction:
        Say.phrase(Responses.map_direction)
        place = None

        while place is None:
            place = SpeechWorker.get_without_capture()
        print(place)
        place_name, directions = Map.get_to_place(place)
        Say.phrase(Responses.place_name(place_name))
        Say.phrase(Responses.directions_intent())

        for direction in directions:
            Say.phrase(direction)

    elif response == Responses.map_current_location:
        current_location = Map.where_am_i()
        for address in current_location:
            Say.phrase(address)

    elif response == Responses.ocr_on:
        OcrObject.flag = True
        Say.phrase(Responses.say_ocr_mode_on)
        OcrObject.ocr_thread = Ocr()
        OcrObject.ocr_thread.start()

    elif response == Responses.stop_ocr:
        OcrObject.flag = False
        OcrObject.ocr_thread.make_scan_page()
        OcrObject.ocr_thread.join()

    elif response == Responses.scan_page:
        if OcrObject.flag:
            Say.phrase(Responses.say_scan_page)
            OcrObject.ocr_thread.make_scan_page()
            ocr_text = OcrObject.ocr_thread.join()
            Say.phrase(ocr_text)
            response_select(Responses.ocr_on)

    elif response == Responses.get_nearest_bus_stop:
        stop_name, directions = Map.get_nearest_bus_stop()
        Say.phrase(Responses.bus_stop_name(stop_name))
        Say.phrase(Responses.directions_intent())

        for direction in directions:
            Say.phrase(direction)

    elif response == Responses.current_time:
        Say.phrase(get_current_time())

    elif response == Responses.name:
        Say.phrase(Responses.name)

    elif response == Responses.hello:
        Say.phrase(Responses.hello)

    else:
        Say.phrase(Responses.not_understand)


def main():
    chat_bot = ChatBot()

    while True:
        word_phrase = SpeechWorker.get()

        #test
        #word_phrase = input()
        if word_phrase is None:
            pass
        else:
            print(word_phrase)
            response = chat_bot.run(input=word_phrase)
            print(response)
            response_select(response=response[Responses.accurate])


if __name__ == '__main__':
    main()
