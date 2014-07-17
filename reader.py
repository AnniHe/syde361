import os
import Queue
import thread
from time import sleep

namePipe = {}
queue = Queue.Queue()

def main():
    print "in main"
    pipe = '/tmp/opi_pipe'
    #makePipe()
    for i in range(1, 11):
        thread.start_new_thread(readPipe, (pipe + str(i),))
    #processing()

    sleep(999)

def processing():
    while not queue.empty():
        print "DEQUEUING....."
        print queue.get()

def makePipe():
    #ensure no pipes

    pipe = '/tmp/opi_pipe'
    for i in range(1, 10):
        namePipe[i] = pipe + str(i)
        if os.path.exists(namePipe[i]):
            os.remove(namePipe[i])
            #os.unlink(namePipe[i])
        os.mkfifo(namePipe[i], 0666)

        #start a thread and pass in the readPipes
        thread.start_new_thread(readPipe, (namePipe[i],))

def readPipe(pipe):
    while not queue.full():
        if not os.path.exists(pipe):
            os.mkfifo(pipe, 0666)
            print "mkfifo" + pipe + "\n"

        print "enter read pipe" + pipe + "\n"
        fd = os.open(pipe, os.O_RDONLY)
        print "opening pipe" + pipe + "\n"
        response = os.read(fd, 2000)
        print response + "\n"
        queue.put(response)
        os.close(fd)
        #os.unlink(pipe)
        print pipe + " unlinked\n"
    else:
        print "queue is full in pipe thread " + pipe + "\n"

main()