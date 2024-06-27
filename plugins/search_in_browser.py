import webbrowser
from synthesize_speech import VoiceSynthesizer


class SearchInBrowser:

    def __init__(self):
        self.phrase_to_search = None

        # Instantiate the VoiceSynthesizer class
        self.synthesizer = VoiceSynthesizer('')


    def keyword_parser(self, command, phrase):
        # Parse the phrase and leave only the words are the command search the internet for
        phrase_parts = phrase.split('for', 1)
        if len(phrase_parts) > 1:
            self.phrase_to_search = phrase_parts[1].strip()
        self.synthesizer.synthesize_speech(f'Searching for {self.phrase_to_search}.')
        self.open_search_default_browser()


    def open_search_default_browser(self):
        # Opens the url
        webbrowser.open_new(f'https://www.google.com/search?q={self.phrase_to_search}')