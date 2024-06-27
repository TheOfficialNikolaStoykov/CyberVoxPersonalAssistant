import tkinter as tk
from views import *
from controller_vosk import *


class CyberVox(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('300x100')
        self.resizable(False, False)

        self.title('Personal Assitant')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create an instance of the HomeView
        home_view = HomeView(self)
        home_view.grid(row=0, column=0, sticky='NSEW', padx=10, pady=10)

        home_view.grid_columnconfigure(0, weight=1)
        home_view.grid_rowconfigure(0, weight=1)

        # Specify the path to the speech model
        speech_model_path = './vosk-model-small-en-us-0.15'

        # Create an instance of the MainController and pass the HomeView and speech model path
        controller = MainController(home_view, speech_model_path)

        # Set the controller for the HomeView
        home_view.set_controller(controller)


if __name__ == '__main__':
    # Create an instance of the CyberVox application
    app = CyberVox()

    # Start the application main loop
    app.mainloop()