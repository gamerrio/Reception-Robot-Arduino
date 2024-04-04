import pyttsx3
import os
import struct
import wave
from datetime import datetime
import speech_recognition as sr
import requests
import json
import pvporcupine
from dotenv import load_dotenv
from pvrecorder import PvRecorder

load_dotenv()
r = sr.Recognizer()
engine = pyttsx3.init()

url = os.getenv('SERVER_URL')  # Set your server URL as an environment variable


def main():
    access_key = os.getenv('ACCESS_KEY')
    print(os.getenv('ACCESS_KEY'))
    keywords = os.getenv('KEYWORDS').split(
        ',') if os.getenv('KEYWORDS') else None
    keyword_paths = os.getenv('KEYWORD_PATHS').split(
        ',') if os.getenv('KEYWORD_PATHS') else None
    library_path = os.getenv('LIBRARY_PATH')
    model_path = os.getenv('MODEL_PATH')
    sensitivities = [float(s) for s in os.getenv('SENSITIVITIES').split(
        ',')] if os.getenv('SENSITIVITIES') else None
    audio_device_index = int(os.getenv('AUDIO_DEVICE_INDEX')) if os.getenv(
        'AUDIO_DEVICE_INDEX') else -1
    output_path = os.getenv('OUTPUT_PATH')
    show_audio_devices = os.getenv(
        'SHOW_AUDIO_DEVICES', 'False').lower() == 'true'

    if show_audio_devices:
        for i, device in enumerate(PvRecorder.get_available_devices()):
            print('Device %d: %s' % (i, device))
        return

    if keyword_paths is None:
        if keywords is None:
            raise ValueError(
                "Either `KEYWORDS` or `KEYWORD_PATHS` must be set.")

        keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in keywords]

    if sensitivities is None:
        sensitivities = [0.5] * len(keyword_paths)

    if len(keyword_paths) != len(sensitivities):
        raise ValueError(
            'Number of keywords does not match the number of sensitivities.')

    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            library_path=library_path,
            model_path=model_path,
            keyword_paths=keyword_paths,
            sensitivities=sensitivities)
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine")
        raise e

    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(
            x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])

    print('Porcupine version: %s' % porcupine.version)

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=audio_device_index)
    recorder.start()

    wav_file = None
    if output_path is not None:
        wav_file = wave.open(output_path, "w")
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)

    print('Listening ... (press Ctrl+C to exit)')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

            if result >= 0:
                print('[%s] Detected %s' %
                      (str(datetime.now()), keywords[result]))
                with sr.Microphone() as source:
                    print("Yes?!")
                    engine.say("yes?")
                    engine.runAndWait()
                    audio = r.listen(source)
                try:
                    e = r.recognize_google(audio)
                    print("you said " + e)
                except sr.UnknownValueError:
                    print("could not understand audio")
                    engine.say("Sorry Could not process that")
                    engine.runAndWait()
                except sr.RequestError as f:
                    print("Sphinx error; {0}".format(f))
                    engine.say("Sorry Could not process that")
                    engine.runAndWait()
                if e:
                    prompt = e
                else:
                    prompt = "Hi, how are you?"
                data = {"prompt": prompt}
                json_data = json.dumps(data)
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, data=json_data, headers=headers)
                if response.status_code == 200:
                    print("Generated response:", response.json()['response'])
                    engine.say(response.json()['response'])
                    engine.runAndWait()
                else:
                    print("Error:", response.text)
                    engine.say(response.text)
                    engine.runAndWait()

    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()


if __name__ == '__main__':
    main()
