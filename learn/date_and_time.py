#!/usr/bin/env python
import time
import datetime


if __name__ == '__main__':
    print datetime.datetime.now()
    time_struct_1 = time.strptime("2017-05-05 15:25:22", '%Y-%m-%d %H:%M:%S')
    print time_struct_1
    seconds_since_epoch = time.mktime(time_struct_1)
    print seconds_since_epoch
    print time.localtime(seconds_since_epoch)
    print time.gmtime(seconds_since_epoch)

