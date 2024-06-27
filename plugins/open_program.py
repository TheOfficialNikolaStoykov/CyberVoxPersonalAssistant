import os
import subprocess
import platform
from synthesize_speech import VoiceSynthesizer
 
 
class OpenProgram:
 
    def __init__(self):
        self.program_name = None
 
        # Define the directories where all the programs are installed
        self.program_dirs_windows = [
            os.environ.get('ProgramFiles'), 
            os.environ.get('ProgramFiles(x86)'),
            os.environ.get('APPDATA'),
            os.environ.get('LOCALAPPDATA'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs')]
 
        self.program_dirs_linux = ['/usr/bin/', '/usr/local/bin', '/usr/share']
 
        self.system = None
 
        # Instantiate the VoiceSynthesizer class
        self.synthesizer = VoiceSynthesizer('')
 
 
    def keyword_parser(self, command, phrase):
        # Parse the phrase and leave everything except the program name: open notion -> Notion
        phrase_parts = phrase.split('open', 1)
        if len(phrase_parts) > 1:
            self.program_name = phrase_parts[1].strip()
        self.program_name = self.program_name[0].upper() + self.program_name[1:]
        self.execute()
 
 
    def execute(self):
        # The main function to execute the open_program plugin
        # Check if the system is Windows or Linux
        self.check_system_os()
        if self.system == 'Windows':
            self.open_program_windows(self.program_name)
        elif self.system == 'Linux':
            self.open_program_linux(self.program_name)
 
 
    def check_system_os(self):
        # Check if the system is Windows or Linux
        self.system = platform.system()
 
 
    def open_program_windows(self, program_name):
        for program_dir in self.program_dirs_windows:
            if program_name == 'chrome':
                program_path = os.path.join(os.environ.get('ProgramFiles'), 'Google', 'Chrome', 'Application', program_name + '.exe')
            else:
                program_path = os.path.join(program_dir, program_name, program_name + '.exe')
 
            if os.path.isfile(program_path):
                # If the file is file, proceed with opening it
                self.synthesizer.synthesize_speech(f'Opening {program_name}.') 
                self.run_program(program_path)   
 
 
    def run_program(self, program_path):
        # Run the program in a subprocess.
        # shell=True - The command is executed through the shell
        # check = True - It will return 'CalledProccessError' if the executed command returns a non-zero exit status.
        subprocess.run(program_path, shell=True, check=True)
 
 
    def open_program_linux(self, program_name):
        program_name = program_name[0].lower() + program_name[1:]
        # Opens a program in Linux with the 'xdg-open' command
        try:
            for program_dir in self.program_dirs_linux:
 
                subprocess.run(['xdg-open',program_dir + program_name], check=True)
        except OSError as e:
            print(f"Error occurred: {str(e)}")