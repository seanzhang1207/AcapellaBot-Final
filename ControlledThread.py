from threading import Thread, Event

class ControlledThread (Thread):

    def __init__(self):
        super(ControlledThread, self).__init__(daemon=True)
        self._run = Event()
        self._run.clear()
        self._unpause = Event()
        self._unpause.set()
        self.setup()

    def run(self):
        self._run.set()
        while self._run.isSet():
            if self._unpause.isSet():
                self.loop()
            else:
                self.onpause()
                self._unpause.wait()
                if self._run.isSet():
                    self.onresume()
        self.onexit()

    def pause(self):
        self._unpause.clear()

    def resume(self):
        self._unpause.set()

    def terminate(self):
        self._run.clear()
        self._unpause.set()

    def setup(self):
        pass

    def loop(self):
        pass

    def onpause(self):
        pass

    def onresume(self):
        pass

    def onexit(self):
        pass


if __name__ == "__main__":
    import time

    class TestControlledThread (ControlledThread):

        def setup(self):
            print("setup")

        def loop(self):
            print(time.time())
            time.sleep(0.25)

        def onpause(self):
            print("pause")

        def onresume(self):
            print("resume")

        def onexit(self):
            print("exit")

    th = TestControlledThread()

    th.start()
    time.sleep(1)
    th.pause()
    time.sleep(1)
    th.resume()
    time.sleep(1)
    th.terminate()
