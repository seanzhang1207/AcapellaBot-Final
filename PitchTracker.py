import aubio
import librosa
from queue import Queue
import time
import numpy as np

from pythonosc import udp_client

from ControlledThread import ControlledThread

class PitchTracker (ControlledThread):

    bufferSize = 2048
    sampleRate = 44100
    tolerance = 0.8

    key = ""

    def setup(self):
        self.Q = Queue()
        self.pitch = 0
        self.confidence = 0
        self.pitches = []

        self._pitch_o = aubio.pitch("default", 4096, self.bufferSize, self.sampleRate)
        self._pitch_o.set_unit("midi")
        self._pitch_o.set_tolerance(self.tolerance)

        self._maxLive = udp_client.SimpleUDPClient('127.0.0.1', 10002)

        print("* Pitch tracker started.")

    def loop(self):
        try:
            data = self.Q.get(block=False)
        except:
            pass
        else:
            t = time.time()

            signal = np.fromstring(data, dtype=np.float32)
            pitch = self._pitch_o(signal)[0]
            confidence = self._pitch_o.get_confidence()

            #print(pitch)

            if confidence > 0.9:

                signal = np.fromstring(data, dtype=np.float32).astype(np.uint16)
                tuning = librosa.estimate_tuning(y=signal, sr=self.sampleRate)

                self.pitch = pitch - tuning
                self.confidence = confidence
                self.pitches.append((self.pitch, self.confidence, t))



            else:
                self.pitch = 0
                self.confidence = 0
        time.sleep(0.00001)

    def onexit(self):
        print("* Pitch tracker stopped.")
