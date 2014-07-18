import os
import Queue
import threading
from time import sleep

queue = Queue.Queue()

def main():
    print "in main"
    pipe = '/tmp/opi_pipe'
    threads = []
    for i in range(1, 11):
        thread = threading.Thread(target=readPipe, args=((pipe + str(i)),))
        threads.append(thread)
        thread.start()
    #processing()

    for t in threads:
        t.join()

    for num in range(1, 11):
        os.remove(pipe + str(num))
    print "main exits"

def processing():
    while not queue.empty():
        print "DEQUEUING....."
        print queue.get()

def readPipe(pipe):
    while not queue.full():
        if not os.path.exists(pipe):
            os.mkfifo(pipe, 0666)

        fd = os.open(pipe, os.O_RDONLY)
        response = os.read(fd, 2000)
        print response + "\n"

        vals = response.split(",")

        for val in vals:
            if val:
                queue.put(response)

        os.close(fd)
    else:
        print "queue is full in pipe thread " + pipe + "\n"

if __name__ == "__main__":
    main()