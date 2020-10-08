import flask
from flask import Flask
app = Flask(__name__)

import speech_recognition as sr
r = sr.Recognizer()

import requests


@app.route('/translate/<audio_file', methods=['POST'])
def request_translation():
    if
