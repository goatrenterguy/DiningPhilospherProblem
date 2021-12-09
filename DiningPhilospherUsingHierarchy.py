import random
import threading
import time


class Philosopher(threading.Thread):
    def __init__(self, leftFork: threading.Semaphore, rightFork: threading.Semaphore, leftVal, rightVal, index, prints=False):
        threading.Thread.__init__(self)
        self.prints = prints
        self.leftFork = leftFork
        self.rightFork = rightFork
        self.leftVal = leftVal
        self.rightVal = rightVal
        self.index = index
        self.running = True
        self.hungryTime = 0

    def run(self):
        while self.running:
            if self.prints:
                print("Philosopher " + str(self.index) + " is thinking")
            time.sleep(random.random())
            # Gets hungry
            if self.prints:
                print("Philosopher " + str(self.index) + " is hungry")
            self.dine()
        print("Philosopher " + str(self.index) + " spent " + str(self.hungryTime) + "m hungry")

    def dine(self):
        # Check larger fork
        if self.leftVal < self.rightVal:
            holdingSmall = False
            holdingBig = False
            start = time.time()
            while not holdingBig:
                holdingBig = self.leftFork.acquire(False)
            if self.prints:
                print("Philosopher " + str(self.index) + " is holding left fork")
            while not holdingSmall:
                holdingSmall = self.rightFork.acquire(False)
            wait = time.time() - start
            if self.prints:
                print("Philosopher " + str(self.index) + " is holding right fork")
        elif self.rightVal < self.leftVal:
            holdingSmall = False
            holdingBig = False
            start = time.time()
            while not holdingBig:
                holdingBig = self.rightFork.acquire(False)
            if self.prints:
                print("Philosopher " + str(self.index) + " is holding right fork")
            while not holdingSmall:
                holdingSmall = self.leftFork.acquire(False)
            wait = time.time() - start
            if self.prints:
                print("Philosopher " + str(self.index) + " is holding left fork")
        if self.prints:
            print("Philosopher " + str(self.index) + " is eating")
        time.sleep(random.random())
        if self.prints:
            print("Philosopher " + str(self.index) + " put down both forks")
        self.leftFork.release()
        self.rightFork.release()
        self.hungryTime += wait



def main():
    forks = [threading.Semaphore() for i in range(5)]
    philosophers = [Philosopher(forks[i % len(forks)], forks[(i + 1) % len(forks)], i % len(forks), (i + 1) % len(forks), i) for i in range(len(forks))]
    for p in philosophers:
        p.start()
    time.sleep(100)
    for p in philosophers:
        p.running = False


if __name__ == "__main__":
    main()