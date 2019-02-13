import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, method, delay):
        super(WorkerThread, self).__init__()
        self.method = method
        self.delay = delay
        self.active = True

    def run(self):
        print("called")
        while self.active:
            print("called")
            self.method()

            if self.delay > 0:
                time.sleep(self.delay)
    
    def stop(self):
        self.active = False
        self.join()
