from flask import Flask, request

app = Flask(__name__)

SAVE_PATH = 'C:\\Users\\Matan\\Desktop\\SaveMe\\harvard.wav'
RECORDING_DICT = {
    'CURR_RECORDING': [],
    'NUM_RECORDING': 0
}

FIRST_SAFE_WORD = 'fluffy'
SECOND_SAFE_WORD = 'cats'


@app.route('/audio', methods=['GET', 'POST'])
def get_audio_file():
    if request.method == 'GET':
        return {
                   'message': 'NICE'
               }, 200
    if request.method == 'POST':
        if request.files['file']:
            # saving file to FS
            save_file_from_request(request)
            audio = get_audio_from_file()
            text: str = translate_audio_to_text(audio)
            RECORDING_DICT['CURR_RECORDING'].append(text.split(' '))
            RECORDING_DICT['NUM_RECORDING'] += 1
            if RECORDING_DICT['NUM_RECORDING'] >= 2:
                if RECORDING_DICT['SHOULD_PING']:
                    return {
                               'message': 'emergency',
                               'action': 'emualate call'
                           }, 200

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


def check_recording_for_sequence():
    first_rec = RECORDING_DICT['CURR_RECORDING'][RECORDING_DICT['NUM_RECORDING'] - 2]
    second_rec = RECORDING_DICT['CURR_RECORDING'][RECORDING_DICT['NUM_RECORDING'] - 1]

    found, where = search_first_word(first_rec, second_rec)
    if found and where == 1:
        if search_second_word_in_both(first_rec, second_rec):
            RECORDING_DICT['SHOULD_PING'] = True
    elif found and where == 2:
        if search_second_word_in_second(second_rec):
            RECORDING_DICT['SHOULD_PING'] = True


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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
