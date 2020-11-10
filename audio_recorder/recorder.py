from threading import Thread, Lock
from pynput import keyboard
import pyaudio,io,random
import wave,queue,os,rootpath
import logging
logger = logging.getLogger(__name__)

class Recorder:
    data = []
    def __init__(self,
                 chunksize=1024,
                 dataformat=pyaudio.paInt16,
                 channels=2,
                 rate=44100):
        self.filename = None
        self.chunksize = chunksize
        self.dataformat = dataformat
        self.channels = channels
        self.rate = rate
        self.recording = False
        self.pa = pyaudio.PyAudio()
        self.wf = None

    def start(self):
        if not self.recording:
            self.filename = 'audio_file' + str(random.randint(0, 10000)) + '.wav'
            try:
                self.wf = wave.open(os.path.join(rootpath.detect(),'output','audio',self.filename), 'wb')
            except IOError:
                logger.exception("I/O error")
            except FileNotFoundError:
                logger.exception("FileNotFoundError")
            except Exception:
                logger.exception("Unexpected error")

            self.wf.setnchannels(self.channels)
            self.wf.setsampwidth(self.pa.get_sample_size(self.dataformat))
            self.wf.setframerate(self.rate)

            def callback(in_data, frame_count, time_info, status):
                self.wf.writeframes(in_data)
                return (in_data, pyaudio.paContinue)

            self.stream = self.pa.open(format=self.dataformat,
                                       channels=self.channels,
                                       rate=self.rate,
                                       input=True,
                                       stream_callback=callback)
            self.stream.start_stream()
            self.recording = True
            logger.info("Recording started")

    def stop(self):
        if self.recording:
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.recording = False
            logger.info("Recording stopped")
            return self.filename

