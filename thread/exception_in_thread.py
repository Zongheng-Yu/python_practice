__author__ = 'zonyu'

from threading import Thread
from time import sleep

def raise_exception():
    raise Exception('exception in thread')


if __name__ == '__main__':
    t = Thread(target=raise_exception)
    while True:
        sleep(1)
        if t:
            t.start()
            t = None
        print '...'
