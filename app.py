#!/bin/python3
from flask import Flask, request
app = Flask(__name__)
import speech_recognition as sr
r = sr.Recognizer()

import copy

SAVE_PATH = 'C:/Users/Matan/SaveMe/harvard.wav'
RECORDING_DICT = {
    'CURR_RECORDING': [],
    'NUM_RECORDING': 0
}

FIRST_SAFE_WORD = 'beer'
SECOND_SAFE_WORD = 'heat'


@app.route('/audio', methods=['GET', 'POST'])
def get_audio_file():
    if request.method == 'GET':
        return {
                   'message': 'NICE'
               }, 200
    if request.method == 'POST':
        if request.files['file']:
            safe_line = return_safe_words_arr(request)
            # saving file to FS
            save_file_from_request(request)
            audio = get_audio_from_file()
            text: str = translate_audio_to_text(audio)
            RECORDING_DICT['CURR_RECORDING'].append(text.split(' '))
            RECORDING_DICT['NUM_RECORDING'] += 1
            if RECORDING_DICT['NUM_RECORDING'] >= 2:
                if check_recording_for_sequence(safe_line):
                    print("FOUND SEQUENCE!")
                    return {
                               'message': 'emergency',
                               'action': 'emualate call'
                           }, 200
        print(RECORDING_DICT['CURR_RECORDING'][0])
        return {'message': 'test'}, 200


def save_file_from_request(flask_req):
    flask_req.files['file'].save(SAVE_PATH)


def get_audio_from_file():
    f = sr.AudioFile(SAVE_PATH)
    audio = None
    with f as source:
        audio = r.record(source)
    return audio


def translate_audio_to_text(audio):
    return r.recognize_google(audio)


def check_recording_for_sequence(safe_line):
    first_rec = RECORDING_DICT['CURR_RECORDING'][RECORDING_DICT['NUM_RECORDING'] - 2]
    second_rec = RECORDING_DICT['CURR_RECORDING'][RECORDING_DICT['NUM_RECORDING'] - 1]
    return search_safe_line_sequence(safe_line, first_rec, second_rec)
    # found, where = search_first_word(first_rec, second_rec)
    # if found and where == 1:
    #     if search_second_word_in_both(first_rec, second_rec):
    #         RECORDING_DICT['SHOULD_PING'] = True
    # elif found and where == 2:
    #     if search_second_word_in_second(second_rec):
    #         RECORDING_DICT['SHOULD_PING'] = True


def search_first_word(first_rec, second_rec):
    for word in first_rec:
        if word == FIRST_SAFE_WORD:
            return True, 1

    for word in second_rec:
        if word == FIRST_SAFE_WORD:
            return True, 2

    return False


def search_second_word_in_both(first_rec, second_rec):
    for word in first_rec:
        if word == SECOND_SAFE_WORD:
            return True

    for word in second_rec:
        if word == SECOND_SAFE_WORD:
            return True

    return False


def search_second_word_in_second(second_rec):
    for word in second_rec:
        if word == SECOND_SAFE_WORD:
            return True
    return False

def return_safe_words_arr(flask_req):
    req_safe_line = flask_req.form['safe_line']
    return req_safe_line.split(' ')

def search_safe_line_sequence(safe_line, first_rec, second_rec):
    safe_line_tracking = copy.copy(safe_line)
    for safe_word in safe_line:
        if safe_word in first_rec:
            safe_line_tracking.remove(safe_word)
            continue
        if safe_word in second_rec:
            safe_line_tracking.remove(safe_word)
    if len(safe_line_tracking) == 0:
        return True
    else:
        return False




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
