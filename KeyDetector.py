import aubio
import librosa
import wave
import subprocess
from threading import Thread, Event
from os.path import join
from os import remove
import re
from queue import Queue
import numpy as np

from ControlledThread import ControlledThread


class EssentiaThread (Thread):

    def __init__(self, frames, id):
        super(EssentiaThread, self).__init__()
        self.frames = frames[:]
        self.path = "temp/" + str(id) + ".wav"
        self.done = Event()
        self.done.clear()
        self.key = None

    def run(self):
        waveFile = wave.open(self.path, 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(2)
        waveFile.setframerate(44100)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

        result = subprocess.run(['essentia/streaming_key', self.path, "temp/output.yaml"], stdout=subprocess.PIPE)
        result = re.findall('[ABCDEFG][b#]*  major|[ABCDEFG][b#]*  minor', result.stdout.decode('utf-8'))

        if len(result) > 0:
            self.key = result[0]

        remove(self.path)

        self.done.set()


class KeyDetector (ControlledThread):

    bufferSize = 2048
    sampleRate = 44100
    tolerance = 0.8
    confidence = 0.9

    def setup(self):
        self.Q = Queue()
        self.key = ""

        self._frames = []
        self._pitch_o = aubio.pitch("default", 4096, self.bufferSize, self.sampleRate)
        self._pitch_o.set_unit("midi")
        self._pitch_o.set_tolerance(self.tolerance)

        self._id = 0
        self._lastKey = ""
        self._stable = 0

        print("* Key detector started.")

    def loop(self):
        if self.key == "":
            try:
                data = self.Q.get(block=False)
            except:
                pass
            else:

                signal = np.fromstring(data, dtype=np.float32)
                pitch = self._pitch_o(signal)[0]
                confidence = self._pitch_o.get_confidence()

                if confidence > self.confidence:

                    print(self._stable)
                    self._frames.append(data)

                    self._id += 1

                    detectorThread = EssentiaThread(self._frames, self._id)
                    detectorThread.start()

                    while not detectorThread.done.isSet():
                        data = self.Q.get()
                        signal = np.fromstring(data, dtype=np.float32)
                        pitch = self._pitch_o(signal)[0]
                        confidence = self._pitch_o.get_confidence()
                        if confidence > self.confidence:
                            self._frames.append(data)

                    if detectorThread.key:
                        print(detectorThread.key)
                        if self._lastKey == detectorThread.key:
                            print(self._stable)
                            self._stable += 1
                            if self._stable > 7:
                                self.key = detectorThread.key
                                print("* Detected key: " + self.key)
                        else:
                            self._stable -= 1
                            if self._stable < 0:
                                self._stable = 0

                        self._lastKey = detectorThread.key
        #else:
            #print(self.key)

    def onexit(self):
        print("* Key detector stopped.")
