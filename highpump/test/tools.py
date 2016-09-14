#!/usr/bin/python
#coding: utf-8
import md5
import datetime
import time

def hash(string):
    return md5.md5(string).hexdigest()

def gettimestamp(dd):
    if isinstance(dd, datetime):
        return time.mktime(dd.timetuple())
    else:
        raise TypeError('Only datetime object can convert to timestamp')


if __name__ == '__main__':
    print hash('123')
