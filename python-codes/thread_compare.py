from threading import Thread
from time import time

class Count:

    def __init__(self, n, threads):
        self.__threads = threads
        self.__n = n

    def run(self):
        # array of all threads created
        all_threads = []
        for i in range(self.__threads):
            # create thread to count n/no_of_threads
            t = Thread(target = self.__count, args = (self.__n//self.__threads, ))
            all_threads.append(t)
        # start timer
        start_time = time()
        # start all threads
        for t in all_threads:
            t.start()
        # block main thread till all threads have completed execution
        for t in all_threads:
            t.join()
        # end timer
        end_time = time()
        return end_time - start_time

    # count till n
    def __count(self, *args):
        i = 0
        n = args[0]
        while i < n:
            i = i + 1

# entrypoint
if __name__ == '__main__':
    # number of threads
    threads = 4
    # count 100 million
    n = 100000000
    for i in range(1, threads+1):
        # init object
        count = Count(n, i)
        print ('time taken to count till %d with %d threads: %f'% (n, i, count.run()))