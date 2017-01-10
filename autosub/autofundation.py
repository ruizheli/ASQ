#!/usr/bin/env python
 #coding=utf-8 
import argparse
import audioop
from googleapiclient.discovery import build
import json
import math
import multiprocessing
import os
import requests
import subprocess
import sys
import tempfile
import wave
import base64

# Import Google Speech API
from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials

from progressbar import ProgressBar, Percentage, Bar, ETA

import sys
import json

import pysrt

text_type = unicode if sys.version_info < (3,) else str

DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')

def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)

def force_unicode(s, encoding="utf-8"):
    if isinstance(s, text_type):
        return s
    return s.decode(encoding)


def srt_formatter(subtitles, show_before=0, show_after=0):
    f = pysrt.SubRipFile()
    for i, (rng, text) in enumerate(subtitles, 1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = force_unicode(text)
        start, end = rng
        item.start.seconds = max(0, start - show_before)
        item.end.seconds = end + show_after
        f.append(item)
    return '\n'.join(map(unicode, f))

def vtt_formatter(subtitles, show_before=0, show_after=0):
    text = srt_formatter(subtitles, show_before, show_after)
    text = 'WEBVTT\n\n' + text.replace(',', '.')
    return text

def json_formatter(subtitles):
    subtitle_dicts = map(lambda (r, t): {'start': r[0], 'end': r[1], 'content': t}, subtitles)
    return json.dumps(subtitle_dicts)

def raw_formatter(subtitles):
    return ' '.join(map(lambda (rng, text): text, subtitles))

FORMATTERS = {
    'srt': srt_formatter,
    'vtt': vtt_formatter,
    'json': json_formatter,
    'raw': raw_formatter,
}

GOOGLE_SPEECH_API_KEY = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
# GOOGLE_SPEECH_API_KEY = "AIzaSyBdrYmI_ZiZ7dey_ymBd-BlLZkw4IvoLZ0"
GOOGLE_SPEECH_API_URL = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang={lang}&key={key}"

LANGUAGE_CODES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'az': 'Azerbaijani',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'et': 'Estonian',
    'eu': 'Basque',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'ga': 'Irish',
    'gl': 'Galician',
    'gu': 'Gujarati',
    'ha': 'Hausa',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hr': 'Croatian',
    'ht': 'Haitian Creole',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'ig': 'Igbo',
    'is': 'Icelandic',
    'it': 'Italian',
    'iw': 'Hebrew',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'ka': 'Georgian',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'kn': 'Kannada',
    'ko': 'Korean',
    'la': 'Latin',
    'lo': 'Lao',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mg': 'Malagasy',
    'mi': 'Maori',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mn': 'Mongolian',
    'mr': 'Marathi',
    'ms': 'Malay',
    'mt': 'Maltese',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'ny': 'Chichewa',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'su': 'Sudanese',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'tg': 'Tajik',
    'th': 'Thai',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'zu': 'Zulu',
}



def percentile(arr, percent):
    arr = sorted(arr)
    k = (len(arr) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c: return arr[int(k)]
    d0 = arr[int(f)] * (c - k)
    d1 = arr[int(c)] * (k - f)
    return d0 + d1


def is_same_language(lang1, lang2):
    return lang1.split("-")[0] == lang2.split("-")[0]


class FLACConverter(object):
    def __init__(self, source_path, include_before=0.25, include_after=0.25):
        self.source_path = source_path
        self.include_before = include_before
        self.include_after = include_after

    def __call__(self, region):
        try:
            start, end = region
            start = max(0, start - self.include_before)
            end += self.include_after
            temp = tempfile.NamedTemporaryFile(suffix='.flac')
            command = ["ffmpeg","-ss", str(start), "-t", str(end - start),
                       "-y", "-i", self.source_path,
                       "-loglevel", "error", temp.name]
            subprocess.check_output(command)
            os.system('stty sane')
            return temp.read()

        except KeyboardInterrupt:
            return


class SpeechRecognizer(object):
    def __init__(self, language="en-IN", rate=44100, retries=3, api_key=GOOGLE_SPEECH_API_KEY):
        self.language = language
        self.rate = rate
        self.api_key = api_key
        self.retries = retries

    def __call__(self, data):
        try:
            for i in range(self.retries):

                speech_content = base64.b64encode(data)
                service = get_speech_service()
                service_request = service.speech().syncrecognize(
                    body={
                        'config': {
                            # There are a bunch of config options you can specify. See
                            # https://goo.gl/KPZn97 for the full list.
                            'encoding': 'FLAC',  # FLAC
                            'sampleRate': self.rate,  # default rate for the audio file
                            'languageCode': self.language,  # a BCP-47 language tag
                        },
                        'audio': {
                            'content': speech_content.decode('UTF-8')
                            }
                        })
                # [END construct_request]
                # [START send_request]
                response = service_request.execute()
                print response
                line = " "
                if response.has_key('results'):
                    for sentences in response['results']:
                        transcript = sentences['alternatives'][0]
                        line = line + transcript['transcript']

                # [END send_request]
                return line[:1].upper() + line[1:]
                # url = GOOGLE_SPEECH_API_URL.format(lang=self.language, key=self.api_key)
                # headers = {"Content-Type": "audio/x-flac; rate=%d" % self.rate}

                # try:
                #     resp = requests.post(url, data=data, headers=headers)
                # except requests.exceptions.ConnectionError:
                #     continue

                # for line in resp.content.split("\n"):
                #     try:
                #         line = json.loads(line)
                #         line = line['result'][0]['alternative'][0]['transcript']
                #         return line[:1].upper() + line[1:]
                #     except:
                #         # no result
                #         continue

        except KeyboardInterrupt:
            return


class Translator(object):
    def __init__(self, language, api_key, src, dst):
        self.language = language
        self.api_key = api_key
        self.service = build('translate', 'v2',
                             developerKey=self.api_key)
        self.src = src
        self.dst = dst

    def __call__(self, sentence):
        try:
            if not sentence: return
            result = self.service.translations().list(
                source=self.src,
                target=self.dst,
                q=[sentence]
            ).execute()
            if 'translations' in result and len(result['translations']) and \
                            'translatedText' in result['translations'][0]:
                return result['translations'][0]['translatedText']
            return ""

        except KeyboardInterrupt:
            return


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def extract_audio(filename, channels=1, rate=16000):
    temp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    if not os.path.isfile(filename):
        print "The given file does not exist: {0}".format(filename)
        raise Exception("Invalid filepath: {0}".format(filename))
    if not which("ffmpeg"):
        print "ffmpeg: Executable not found on machine."
        raise Exception("Dependency not found: ffmpeg")
    command = ["ffmpeg", "-y", "-i", filename, "-ac", str(channels), "-ar", str(rate), "-loglevel", "error", temp.name]
    subprocess.check_output(command)
    return temp.name, rate