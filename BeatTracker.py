import socket
import time
from pythonosc import udp_client

from ControlledThread import ControlledThread

class BeatTracker (ControlledThread):

    beatTimes = []
    bpm = 0
    spb = 0
    windowSize = 3

    def setup(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(('0.0.0.0', 10001))
        self._socket.setblocking(0)
        print("* Beat tracker started.")

        self._maxLive = udp_client.SimpleUDPClient('127.0.0.1', 10002)

    def loop(self):
        try:
            data = self._socket.recv(1024)
        except:
            pass
        else:
            self.beatTimes.append(time.time())
            window = self.beatTimes[-self.windowSize:]
            tmpspb = 0
            for i in range(len(window) - 1):
                tmpspb += window[i+1] - window[i]
            if len(window) - 1 > 0:
                tmpspb /= len(window) - 1
                self.bpm = 60 / tmpspb
                self.spb = tmpspb
                self._maxLive.send_message("/beat", self.bpm)
                self._maxLive.send_message("/mspb", int(self.spb * 1000))
                #print(self.bpm, self.spb)
        time.sleep(0.00001)

    def onexit(self):
        print("* Beat tracker stopped.")

if __name__ == '__main__':
    beatTracker = BeatTracker()
    beatTracker.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        beatTracker.terminate()
        beatTracker.join()
