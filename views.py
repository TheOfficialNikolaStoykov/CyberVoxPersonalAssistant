from tkinter import *
from tkinter import ttk


class HomeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Dictionary to store the command : function references
        self.callbacks = {}
        self.controller = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0, sticky='NSEW')
        self.container.grid_rowconfigure(0, weight=0)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Record button
        self.button_record = ttk.Button(self.container, text='Record')
        self.button_record.grid(row=0, column=0, sticky='NSEW', pady=10)

        # Stop buton
        # self.button_stop = ttk.Button(self.container_right, text='Stop')
        # self.button_stop.grid(row=1, column=0, sticky='E', pady=10)


    def set_controller(self, controller):
        # Set the controller, which is passed in the app.py
        self.controller = controller

    
    def add_callback(self, key, method):
        # Add a command : function reference in the dictionary
        self.callbacks[key] = (method)


    def bind_commands(self):
        # Add the functions for the buttons in the dictionary so they can be called from the controller
        self.button_record.config(command=self.callbacks['start_listening'])
        # self.button_stop.config(command=self.callbacks['stop_listening'])