# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, request

app = Flask(__name__)

import speech_recognition as sr
r = sr.Recognizer()

@app.route('/audio', methods=['GET', 'POST'])
def get_audio_file():
    request.files['file'].save("C:/Users/Matan/Desktop/bla/harvard.wav")
    f = sr.AudioFile("C:/Users/Matan/Desktop/bla/harvard.wav")
    with f as source:
        audio = r.record(source)
    print(type(f))
    if request.method == 'GET':
        return {
                   'message': 'NICE'
               }, 200
    if request.method == 'POST':
        return r.recognize_google(audio), 200


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
