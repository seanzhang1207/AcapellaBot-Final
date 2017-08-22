import pyaudio
import numpy as np

from ControlledThread import ControlledThread
from KeyDetector import KeyDetector

class AudioSampleDispatcher (ControlledThread):

    def setup(self):
        self.audioPort = pyaudio.PyAudio()
        self._bufferSize = 2048
        self._sampleFormat = pyaudio.paFloat32
        self._nChannels = 1
        self._sampleRate = 44100

        self._stream = self.audioPort.open(
            format = self._sampleFormat,
            channels = self._nChannels,
            rate = self._sampleRate,
            input = True,
            frames_per_buffer = self._bufferSize
        )

        self.keyDetector = KeyDetector()

    def loop(self):
        buffer = self._stream.read(self._bufferSize)

        self.keyDetector.Q.put(buffer)

if __name__ == "__main__":
    import time
    d = AudioSampleDispatcher()
    d.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        d.terminate()
