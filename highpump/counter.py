#!/usr/bin/python
#coding: utf-8
from error import InternalError

CounterDict = {}


class Counter(object):
    '''
    得到长度为N的一个计数器, 一次全局自增1    
    '''
    def __init__(self, n):
        self.max_num = n
        self.cnt = 0


    def count(self):
        self.cnt += 1
        if len(str(self.cnt)) > self.max_num:
            self.cnt = 0
        return self


    def __str__(self):
        return "%s" % (str(self.cnt).zfill(self.max_num))



def get_counter(key):
    if not CounterDict.has_key(key):
        raise InternalError(-10002, "Counter key %s doesn't exist." % key)
    return CounterDict[key]


def create_counter(key, n):
    if CounterDict.has_key(key):
        raise InternalError(-10001, "counter key %s has already existed." % key)
    CounterDict[key] = Counter(n)
    return CounterDict[key]


if __name__ == "__main__":
    a = create_counter("a", 1)
    b = create_counter("b", 10)
    try:
        c = create_counter("a", 1)
    except InternalError as e:
        print "internal error: %d:%s" % (e.errcode, e.errmsg)
    a.count()
    a.count()
    b.count()
    d = get_counter("a")
    print str(d)
    print str(b)
    try:
        e = get_counter("e")
    except InternalError as e:
        print "internal error: %d:%s" % (e.errcode, e.errmsg)
