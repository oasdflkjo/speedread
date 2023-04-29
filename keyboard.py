import pygetwindow
from pynput import keyboard


class KeyboardListener:
    def __init__(self, pause_callback):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.pause_callback = pause_callback
        self.is_paused = False

    def on_press(self, key):
        if key == keyboard.Key.space and self.is_program_window_focused():
            self.is_paused = not self.is_paused
            self.pause_callback(key, self.is_paused)

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()

    def is_program_window_focused(self):
        active_window = pygetwindow.getActiveWindow()
        program_window = pygetwindow.getWindowsWithTitle(
            "Word Viewer")
        return active_window in program_window
