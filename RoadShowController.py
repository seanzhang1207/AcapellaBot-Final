import time
from pythonosc import udp_client
from threading import Event

from ControlledThread import ControlledThread
from AudioSampleDispatcher import AudioSampleDispatcher
from LearnSong import LearnSong
from SingAlong import SingAlong

class RoadShowController (ControlledThread):

    def waitForTime(self, t):
        self.waitingTime = t
        self.waitingStartTime = time.time()

    def waitOnSignal(self, sig):
        self.waitingSignal = sig

    def saySentence(self, id):
        self._maxLive.send_message("/say", id)

    def stage_1(self):
        self.interactionStage = 1
        print("*** Saying: Hi there, Parvar look!")
        self.saySentence(1)
        self.waitForTime(5)
        # Wait for the other robot to respond
        self.interactionStage += 1

    def stage_2(self):
        self.interactionStage = 2
        print("*** Saying: Hi I'm Rotty. I sing soprano. We're AcapellaBots. Hey, together we can form a choir! What do you want to sing?")
        self.saySentence(2)
        self.waitForTime(5)
        if self.doSpeechRecognition.isSet():
            self.waitForTime(5)
        else:
            self.waitOnSignal(self.fakeSpeechRecogSignal)
        self.interactionStage += 1

    def stage_3(self):
        self.interactionStage = 3
        #error.empty
        self.interactionStage += 1

    def stage_4(self):
        self.interactionStage = 4
        print("*** (Got user input - song name)")
        print("*** Saying: Oh I don't know that song yet... Come on! Teach me!")
        self.saySentence(4)
        self.learnSong = LearnSong()
        self.learnSong.start()
        self.waitForTime(5)
        self.interactionStage += 1

    def stage_5(self):
        self.interactionStage = 5
        self.waitOnSignal(self.learnSong.learned)
        self.interactionStage += 1

    def stage_6(self):
        self.interactionStage = 6
        if self.learnSong.key != "":
            print(self.learnSong.key)
            learned = True
            self.key = self.learnSong.key
            self.interactionStage += 1
        else:
            print("*** Saying: Um I haven't quite got it... Could you sing it again?")
            self.saySentence(5)
            self.waitTime = 5


    def stage_7(self):
        self.interactionStage = 7
        print("*** (Got user input - song)")
        print("*** Saying: Ok I think I know it by heart already! Smart me. I'm ready to acapella, just say \"start\" when you're ready, and use the baton to coordinate!")
        self.saySentence(6)
        self.waitForTime(5)
        # wait for user to say start here
        self.interactionStage += 1

    def stage_8(self):
        self.interactionStage = 8
        print("*** (Got user input - start)")
        singAlong = SingAlong()
        singAlong.key = self.key
        singAlong.start()
        self.waitOnSignal(singAlong.done)
        self.interactionStage += 1

    def stage_9(self):
        self.interactionStage = 9
        print("*** (Got user input - done)")
        print("*** Saying: Wow we nailed it! Now I'll go show it off! Thank you!")
        self.saySentence(7)
        self.waitForTime(5)
        print("*** (End of road show)")
        self.interactionStage = 7

    def setup(self):
        print("* Starting new road-show session.")
        self._maxLive = udp_client.SimpleUDPClient('127.0.0.1', 10002)

        self.doSpeechRecognition = Event()
        self.doSpeechRecognition.clear()

        self.doStage1 = Event()
        self.doStage1.set()

        self.doStage2 = Event()
        self.doStage2.set()

        self.doStage3 = Event()
        self.doStage3.set()

        self.doStage4 = Event()
        self.doStage4.set()

        self.doStage5 = Event()
        self.doStage5.set()

        self.doStage6 = Event()
        self.doStage6.set()

        self.doStage7 = Event()
        self.doStage4.set()

        self.doStage8 = Event()
        self.doStage5.set()

        self.doStage9 = Event()
        self.doStage6.set()

        self.fakeSpeechRecogSignal = Event()
        self.fakeSpeechRecogSignal.clear()

        self.waitingTime = 0
        self.waitingStartTime = 0
        self.waitingSignal = None

        self.interactionStage = 0

        self.learnSong = None
        self.singAlong = None

    def loop(self):
        if self.waitingTime != 0 and self.waitingStartTime != 0:
            if time.time() - self.waitingStartTime > self.waitingTime:
                self.waitingTime = 0
                self.waitingStartTime = 0
            else:
                return

        if self.waitingSignal != None:
            if self.waitingSignal.isSet():
                self.waitingSignal = None
            else:
                return

        if self.interactionStage == 1 and self.doStage1.isSet():
            self.stage_1()
        elif self.interactionStage == 2 and self.doStage2.isSet():
            self.stage_2()
        elif self.interactionStage == 3 and self.doStage3.isSet():
            self.stage_3()
        elif self.interactionStage == 4 and self.doStage4.isSet():
            self.stage_4()
        elif self.interactionStage == 5 and self.doStage5.isSet():
            self.stage_5()
        elif self.interactionStage == 6 and self.doStage6.isSet():
            self.stage_6()
        elif self.interactionStage == 7 and self.doStage7.isSet():
            self.stage_7()
        elif self.interactionStage == 8 and self.doStage8.isSet():
            self.stage_8()
        elif self.interactionStage == 9 and self.doStage9.isSet():
            self.stage_9()

    def onexit(self):
        print("* Exiting road show session...")
        if self.learnSong != None:
            self.learnSong.terminate()
            self.learnSong.join()
            self.singAlong.terminate()
            self.learnSong.join()

if __name__ == "__main__":
    rsc = RoadShowController()
    rsc.start()
    rsc.interactionStage = 1

    rsc.join()
