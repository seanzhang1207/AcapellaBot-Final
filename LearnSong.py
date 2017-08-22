import time
import pyaudio
import mingus.core.notes as notes
import mingus.core.scales as scales
import mingus.core.intervals as intervals
from pythonosc import udp_client
from threading import Event

from ControlledThread import ControlledThread
from KeyDetector import KeyDetector
from PitchTracker import PitchTracker
from BeatTracker import BeatTracker
from TimeMeasureDetector import TimeMeasureDetector

class LearnSong (ControlledThread):

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
        self.keyDetector.start()

        self.learned = Event()
        self.learned.clear()

    def loop(self):
        buffer = self._stream.read(self._bufferSize)

        self.keyDetector.Q.put(buffer)

        if self.keyDetector.key != "":
            self.key = self.keyDetector.key
            self.terminate()
        time.sleep(0.00001)


    def onexit(self):
        self.keyDetector.terminate()
        self.keyDetector.join()
        self._stream.stop_stream()
        self._stream.close()
        self.audioPort.terminate()

if __name__ == "__main__":
    import time
    learned = False
    while not learned:
        learnSong = LearnSong()
        learnSong.start()
        learnSong.join()
        if learnSong.key != "":
            print(learnSong.key)
            learned = True
