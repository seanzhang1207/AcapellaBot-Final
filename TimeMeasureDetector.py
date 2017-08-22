import numpy as np
from ControlledThread import ControlledThread
import mingus.core.notes as notes
import mingus.core.scales as scales

class TimeMeasureDetector (ControlledThread):

    beatTracker = None
    pitchTracker = None
    keyDetector = None

    def setup(self):
        self.timeMeasure = ""
        print("* Time measure detector started.")

    def loop(self):
        if self.beatTracker and self.pitchTracker and self.keyDetector:
            if self.keyDetector.key != "" and self.beatTracker.bpm > 0:
                # Grab current data
                pitches = self.pitchTracker.pitches[:]
                beats = self.beatTracker.beatTimes[:]
                bpm = self.beatTracker.bpm
                spb = self.beatTracker.spb
                key = self.keyDetector.key[0]
                majorMinor = self.keyDetector.key[-5:]

                # Generate scale from key
                if majorMinor == "major":
                    scale = scales.get_notes(key)
                else:
                    scale = scales.get_notes(notes.reduce_accidentals(key + "###"))
                    scale[4] = notes.reduce_accidentals(scale[4] + "#")

                # Divide pitch data into packets with the help of beat data
                packets = []
                packet = []
                beat = 0
                for pitchData in pitches:
                    if pitchData[2] < beats[beat]:
                        packet.append(pitchData)
                    else:
                        if len(packet) > 0:
                            packets.append(packet)
                        packet = [pitchData]
                        if beat < len(beats) - 1:
                            beat += 1

                # Turn each packet into consistent notes
                f = open("testdata.py", 'w')
                f.write(repr(packets))
                f.close()

    def onexit(self):
        print("* Time measure detector stopped.")
