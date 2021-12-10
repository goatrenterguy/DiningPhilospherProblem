import queue
import random
import threading
import time


class Philosopher(threading.Thread):
    def __init__(self, waiter, index, prints=False):
        threading.Thread.__init__(self)
        self.prints = prints
        self.waiter = waiter
        self.index = index
        self.running = True
        self.hungryTime = 0

    # The philosopher, while running, makes requests to the waiter when hungry
    def run(self):
        while self.running:
            time.sleep(random.random())
            ate = self.waiter.request(self)
        print("Philosopher " + str(self.index) + " spent " + str(self.hungryTime) + "s hungry")

    # A philosopher given permission can eat
    def dine(self):
        if self.prints:
            print("Philosopher " + str(self.index) + " is eating")

    # If permission is not granted, the philosopher must wait
    def wait(self):
        if self.prints:
            print("The waiter is busy, philosopher " + str(self.index) + " will eat when the waiter is ready.")
        wait = random.random()
        self.hungryTime += wait
        time.sleep(wait)


class Waiter:
    def __init__(self):
        self.serving = False
        self.requests = []

    # When a request is made to the waiter, if the waiter is not serving
    # then the philosopher may dine. If the waiter is currently serving,
    # then the philosopher is added to a queue and must wait until
    # resources are available.
    def request(self, p: Philosopher):
        if p not in self.requests:
            self.requests.append(p)
        if not self.serving:
            self.serve(self.requests[0])
            self.requests.remove(self.requests[0])
        else:
            p.wait()

    def serve(self, p: Philosopher):
        self.serving = True
        p.dine()
        self.serving = False


def main():
    waiter = Waiter()
    philosophers = [Philosopher(waiter, i) for i in range(5)]
    for p in philosophers:
        p.start()
    time.sleep(100)
    for p in philosophers:
        p.running = False


if __name__ == "__main__":
    main()
