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

    def run(self):
        while self.running:
            #print("Philosopher " + str(self.index) + " is thinking")
            time.sleep(random.random())
            # Gets hungry
            #print("Philosopher " + str(self.index) + " is hungry")
            self.waiter.request(self)
        print("Philosopher " + str(self.index) + " spent " + str(self.hungryTime) + "ms hungry")


    def dine(self):
        print("Philosopher " + str(self.index) + " is eating")
        wait = random.random()
        self.hungryTime += wait
        time.sleep(wait)

    def wait(self):
        print("The waiter is busy, philosopher " + str(self.index) + " will eat when the waiter is ready.")

class Waiter:
    def __init__(self):
        self.serving = False
        self.requests = []

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
