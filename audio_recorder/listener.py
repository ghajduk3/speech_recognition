from threading import Thread, Lock
from pynput import keyboard
import pyaudio,queue
import wave,io

class Listener(keyboard.Listener):
    def __init__(self, recorder, player):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.recorder = recorder
        self.player = player
        self.audio_path = None

    def on_press(self, key):
        if key is None:  # unknown event
            pass
        elif isinstance(key, keyboard.Key):  # special key event
            if key.ctrl and self.player.playing == 0:
                self.recorder.start()
        # elif isinstance(key, keyboard.KeyCode):  # alphanumeric key event
        #     if key.char == 'q':  # press q to quit
        #         if self.recorder.recording:
        #             self.recorder.stop()
        #         return False  # this is how you stop the listener thread
        #     if key.char == 'p' and not self.recorder.recording:
        #         self.player.start(self.audio_path)

    def on_release(self, key):
        if key is None:  # unknown event
            pass
        elif isinstance(key, keyboard.Key):  # special key event
            if key.ctrl:
                self.audio_path = self.recorder.stop()
                return False
