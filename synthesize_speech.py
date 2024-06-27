"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from pygame import mixer


class VoiceSynthesizer():

    def __init__(self, text_input):
        self.client = None
        self.synthesis_input = None
        self.voice = None
        self.audio_config = None
        self.text_input = text_input


    def instantiate_client(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient.from_service_account_json('./google_text_to_speech_key.json')


    def set_text(self, text_input: str):
        # Set the text input to be synthesized
        self.synthesis_input = texttospeech.SynthesisInput(text=text_input)


    def build_voice_request(self):
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        self.voice = texttospeech.VoiceSelectionParams(
            language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )


    def select_audio_type(self):
        # Select the type of audio file you want returned
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )


    def perform_tts(self):
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=self.synthesis_input, voice=self.voice, audio_config=self.audio_config
        )

        # The response's audio_content is binary.
        with open("./output.mp3", 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)


        self.play_saved_file()


    def play_saved_file(self):
        # Path to the sound file
        sound_file = './output.mp3'
        
        pygame_mixer = mixer
        pygame_mixer.init()
        pygame_mixer.music.load(sound_file)
        pygame_mixer.music.play()


    def synthesize_speech(self, text):
        self.set_text(text)
        self.instantiate_client()
        self.build_voice_request()
        self.select_audio_type()
        self.perform_tts()