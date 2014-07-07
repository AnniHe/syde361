import os
import cPickle
import Queue
from threading import Thread 
import time

queue = Queue.Queue()

def main():
        #try:
	#	thread.start_new_thread(piping)
	#	thread.start_new_thread(processing)
	#except:
        #	print "Thread could not start"
	ReadPipe(2)
	processing()
	
def piping():
	for i in range(10):
		ReadPipe(i)

def processing():
	while not queue.empty():
		print queue.get()

		
def ReadPipe(i):
	#pipe = str.join("/tmp/mypipe", i)
	pipe = "/tmp/mypipe"
	try:
		os.mkfifo(pipe)
	except OSError:
		pass
	rpipe = open(pipe, 'r')
	response = rpipe.read()
	queue.put(response)
	print "piping:%s" % response
		
if __name__== '__main__':
	main()




