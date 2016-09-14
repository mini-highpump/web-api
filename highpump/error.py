#!/usr/bin/python
#coding: utf-8


class BaseError(Exception):
    '''
    Base error. 
    '''
    def __init__(self, errcode, errmsg):
        self.__errcode = errcode
        self.__errmsg = errmsg


    @property
    def errcode(self):
        return self.__errcode


    @property
    def errmsg(self):
        return self.__errmsg


class InternalError(BaseError):
    '''
    Internal server error.
    This type of errors must be logged and return it's value.
    '''
    def __init__(self, errcode, errmsg):
        BaseError.__init__(self, errcode, errmsg)


class ThrownError(BaseError):
    '''
    Error which can be thrown directly indicates it isn\'t so emergent.
    '''
    def __init__(self, errcode, errmsg):
        BaseError.__init__(self, errcode, errmsg)
