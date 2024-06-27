import json
import pyaudio
from vosk import Model, KaldiRecognizer
from loader import Loader
from re import sub
from pygame import mixer
from threading import Thread
from time import sleep
from synthesize_speech import VoiceSynthesizer


class MainController:

    def __init__(self, view, speech_model_path):

        # Execute the view's function to add a command : function reference
        view.add_callback('start_listening', self.start_listening)
        view.add_callback('stop_listening', self.stop_listening)

        # Execute the view's function to bind the buttons with the corresponding functions
        view.bind_commands()

        # Create an instance of the Loader class
        self.loader = Loader()

        # Execute the function to load the plugins
        self.loader.load_plugins()


        # Load the Vosk speech model
        self.model = Model(speech_model_path)
        self.rec = None

        # Get the factory which is instantiated in the Loader
        self.factory = self.loader.factory

        self.phrase = None
        self.thread_running = False

        # Initialize the pygame mixer in order to play sound
        self.pygame_mixer = mixer
        self.pygame_mixer.init()

        # Instantiate the VoiceSynthesizer class
        self.synthesizer = VoiceSynthesizer('')

        

    def play_introductory_voice(self):
        sleep(1)
        # Play the an introductory phrase
        self.synthesizer.synthesize_speech('Hello! What can I assist you with? Please speak now.')
        sound_file = './output.mp3'
        self.pygame_mixer.music.load(sound_file)
        self.pygame_mixer.music.play()
    

    def speech_to_text(self):
        # Instantiate PyAduio class
        py_audio = pyaudio.PyAudio()

        # Open a stream with the required arguments
        stream = py_audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=8192)

        # Start the stream
        stream.start_stream()

        # Instantiate the KaliRecognizer class and pass the model and sampling frequency
        self.rec = KaldiRecognizer(self.model, 44100)

        # Desired listening duration in seconds
        timeout = 35
        
        # Track the duration of listening
        duration = 0

        # Desired timeout duration in seconds
        silence_timeout = 31

        # Track the duration of silence
        silence_duration = 0

        while self.thread_running and duration < timeout and silence_duration < silence_timeout:
            # Read the data from the audio stream - 4000 frames of audio
            data = stream.read(4000, exception_on_overflow=False)
            # If there's nothing that came as data from the audio stream, break the while loop
            if len(data) == 0:
                break
            # Accepts a waveform and returns the recognized text
            if self.rec.AcceptWaveform(data):
                # Extract the result from the json
                result = self.rec.Result()
                result = json.loads(result)
                phrase = result['text']
                self.keyword_parser_main(phrase)

                # Reset the silence duration when speech is detected
                silence_duration = 0
            else:
                # Increment silence duration when no speech is detected
                silence_duration += 4000 / 16000

            # Update the duration based on the amount of audio read
            duration += 4000 / 16000


        if duration >= timeout:
            print('Listening duration reached')
            self.keyword_parser_main(phrase)
            self.stop_listening()
            

        if silence_duration >= silence_timeout:
            print('Silence timeout reached')
            self.stop_listening()

        

    def start_listening(self):
        # Start a new thread and with the speech_to_text function
        self.play_introductory_voice()
        self.thread_running = True
        print('Thread started')
        recording_thread = Thread(target=self.speech_to_text)
        recording_thread.start()


    def stop_listening(self):
        # Stop the running thread
        self.thread_running = False
        print('Thread stopped')
        sleep(1)

    
    def keyword_parser_main(self, phrase: str):
        # Extract only words and make them lowercase
        phrase = sub(r'[^\w\s]', '', phrase.lower())
        print(phrase)

        self.plugin_activation(phrase)


    def plugin_activation(self, phrase):
        # Activate the plugins based on the commands in the configuration.json file
        for command in self.loader.factory.command_instance_references.keys():
            if command in phrase:
                class_instance = self.loader.factory.return_class_instance(command)
                class_instance.keyword_parser(command=command, phrase=phrase)
                sleep(5)
                self.stop_listening()