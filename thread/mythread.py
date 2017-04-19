import threading
from time import sleep
import logging

logger = logging.getLogger(__name__)


def write_log():
    while True:
        logger.warning("I am sub thread. Hello")
        sleep(0.1)


def print_a():
    while True:
        print 'hello, hello, hello, hello'

def print_b():
    while True:
        print 'kitty, kitty, kitty, kitty'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # write_log()
    threading.Thread(target=print_a).start()
    print_b()
