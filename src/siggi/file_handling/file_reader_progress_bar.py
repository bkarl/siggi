import time
from tkinter import ttk
import tkinter as tk


class FileReaderProgressBar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading File")
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=350, mode='determinate')
        self.progress_bar.pack(pady=20)
        self.root.geometry("400x100")
        self.progress = 0
        self.progress_max = 0
        self.run = True

    def set_max(self, new_max):
        self.progress_max = new_max

    def update(self):
        self.progress += 1

    def update_progress_bar(self):
        self.progress_bar['maximum'] = self.progress_max
        self.progress_bar['value'] = self.progress

    def close(self):
        self.run = False

    def render(self):
        while self.run:
            self.root.update()
            self.update_progress_bar()
            time.sleep(0.1)
        self.root.destroy()