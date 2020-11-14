from pynput import keyboard

class Listener(keyboard.Listener):
    """
    A class to represent a keyboard listener. Inherits keyboard.Listener class

    ...

    Attributes
    ----------
    recorder : audio_recorder.recorder.Recorder
        instance of recorder object

    Methods
    -------
    on_press(key):
        invokes recorder.start() method while key is pressed.
    on_release(key):
        invokes recorder.stop() method while key is released. Stops/closes the listener thread.
    """
    def __init__(self, recorder):
        """
        Invokes parent's constructor. Constructs all the necessary attributes for the listener object.

        Parameters
        ----------
            recorder : audio_recorder.recorder.Recorder
                instance of recorder object
        """
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.recorder = recorder
        self.audio_path = None

    def on_press(self, key):
        '''
        Invokes recorder.start() method while key is pressed.

                Parameters:
                        key (pynput.keyboard.Key): A keyboard key
        '''
        if key is None:
            pass
        elif isinstance(key, keyboard.Key):
            if key.ctrl:
                self.recorder.start()

    def on_release(self, key):
        '''
        Invokes recorder.stop() method while key is released. Stops/closes the listener thread.

                Parameters:
                        key (pynput.keyboard.Key): A keyboard key
        '''
        if key is None:
            pass
        elif isinstance(key, keyboard.Key):
            if key.ctrl:
                self.audio_path = self.recorder.stop()
                return False
