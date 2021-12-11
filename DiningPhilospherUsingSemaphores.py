import random
import threading
import time


class Philosopher(threading.Thread):
    def __init__(self, leftFork: threading.Semaphore, rightFork: threading.Semaphore, index, prints=False):
        threading.Thread.__init__(self)
        self.prints = prints
        self.leftFork = leftFork
        self.rightFork = rightFork
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
        print("Philosopher " + str(self.index) + " spent " + str(self.hungryTime) + "s hungry")

    def dine(self):
        # Check left fork
        holdingRight = False
        holdingLeft = self.leftFork.acquire(False)
        if holdingLeft:
            if self.prints:
                print("Philosopher " + str(self.index) + " is holding left fork")
            holdingRight = self.rightFork.acquire(False)
        if holdingRight:
            if self.prints:
                print("Philosopher " + str(self.index) + " is holding right fork")
        if holdingLeft and holdingRight:
            if self.prints:
                print("Philosopher " + str(self.index) + " is eating")
            time.sleep(random.random())
            count += 1
            if self.prints:
                print("Philosopher " + str(self.index) + " put down both forks")
            self.leftFork.release()
            self.rightFork.release()
        else:
            if self.prints:
                print("Philosopher " + str(self.index) + " put down left fork")
            self.leftFork.release()
            wait = random.random()
            self.hungryTime += wait
            time.sleep(wait)
            self.dine()


def main():
    forks = [threading.Semaphore() for i in range(5)]
    philosophers = [Philosopher(forks[i % len(forks)], forks[(i + 1) % len(forks)], i) for i in range(len(forks))]
    for p in philosophers:
        p.start()


if __name__ == "__main__":
    main()
