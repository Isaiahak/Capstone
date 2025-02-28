import tkinter as tk
import time 

class Notifications(tk.Label):
    def __init__(self, message, type):
        self.message = message
        self.notification_type = type
        self.timer = None
        self.frame = None
        self.timer = None

    def create(self, parent_frame):
        self.frame = tk.Label(parent_frame, text=self.message, font=("Courier",12))
        self.frame.pack(padx=5, pady=5)
        self.timer = time.time()

    def get_creation_time(self):
        return self.timer

    def get_notification_type(self):
        return self.notification_type

    def get_frame(self):
        return self.frame