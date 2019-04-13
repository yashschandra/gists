from threading import Thread
from time import time

class Count:

    def __init__(self, n, threads):
        self.__threads = threads
        self.__n = n

    def run(self):
        all_threads = []
        for i in range(self.__threads):
            t = Thread(target = self.__count, args = (self.__n//self.__threads, ))
            all_threads.append(t)
        start_time = time()
        for t in all_threads:
            t.start()
        for t in all_threads:
            t.join()
        end_time = time()
        return end_time - start_time

    def __count(self, *args):
        i = 0
        n = args[0]
        while i < n:
            i = i + 1

if __name__ == '__main__':
    threads = 4
    n = 100000000
    for i in range(1, threads+1):
        count = Count(n, i)
        print ('time taken to count till %d with %d threads: %f'% (n, i, count.run()))