#!/usr/bin/env python
import logging
import threading
from time import sleep
from thread.mythread import write_log

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', level=logging.DEBUG)


def main_loop():
    while True:
        logger.warning("I am main thread. I am feeling lucky")
        sleep(0.1)


if __name__ == '__main__':
    threading.Thread(target=write_log).start()
    logger.warning('main begin')
    main_loop()
