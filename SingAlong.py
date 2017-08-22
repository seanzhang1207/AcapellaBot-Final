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

class SingAlong (ControlledThread):

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

        self.pitchTracker = PitchTracker()
        self.pitchTracker.start()

        self.beatTracker = BeatTracker()
        self.beatTracker.start()
        """
        self.timeMeasureDetector = TimeMeasureDetector()
        self.timeMeasureDetector.pitchTracker = self.pitchTracker
        self.timeMeasureDetector.keyDetector = self.keyDetector
        self.timeMeasureDetector.beatTracker = self.beatTracker
        self.timeMeasureDetector.start()
        """
        self._maxLive = udp_client.SimpleUDPClient('127.0.0.1', 10002)
        self._noAudio = 0

        self.done = Event()
        self.done.clear()
        print("* Singing along...")

    def loop(self):
        buffer = self._stream.read(self._bufferSize)

        self.pitchTracker.Q.put(buffer)

        pitch = int(round(self.pitchTracker.pitch))

        if self.key != "":
            key = self.key[0]
            majorMinor = self.key[-5:]

            # Generate scale from key
            if majorMinor == "major":
                scale = scales.get_notes(key)
            else:
                scale = scales.get_notes(notes.reduce_accidentals(key + "###"))
                scale[4] = notes.reduce_accidentals(scale[4] + "#")

            note = notes.reduce_accidentals(notes.int_to_note(pitch % 12))
            if not note in scale:
                minDiff = 1000
                dPitch = 0
                for n in scale:
                    diff = abs(notes.note_to_int(n) - notes.note_to_int(note))
                    if diff < minDiff:
                        minDiff = diff
                        dPitch = notes.note_to_int(n) - notes.note_to_int(note)
                pitch += dPitch
            print(pitch)

            if pitch > 10:
                self._noAudio = 0
                self._maxLive.send_message("/pitch", pitch)
                self._maxLive.send_message("/key", notes.note_to_int(key))
            else:
                self._noAudio += 1
                print("*** No Audio! " + str(self._noAudio))
                if self._noAudio > 100:
                    self.done.set()
                    self.terminate()

        time.sleep(0.00001)


    def onexit(self):
        self.pitchTracker.terminate()
        self.beatTracker.terminate()
        #self.timeMeasureDetector.terminate()

        self.pitchTracker.join()
        self.beatTracker.join()
        #self.timeMeasureDetector.join()

        self._stream.stop_stream()
        self._stream.close()
        self.audioPort.terminate()

if __name__ == "__main__":
    singAlong = SingAlong()
    singAlong.key = "someKey"
    singAlong.start()
    singAlong.join()
