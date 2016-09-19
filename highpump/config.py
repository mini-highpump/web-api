#!/usr/bin/python
#coding: utf-8
class BaseConfig(object):
    '''Base config'''
    SQLALCHEMY_DATABASE_URI = 'mysql://root:a767813944@localhost/highpump'
    # 分表的N的值
    TABLE_NUM = 7

    HOST = "http://119.29.247.130"

    SQLALCHEMY_ECHO = True


class DevelopmentConfig(BaseConfig):
    '''Development mode'''
    DEBUG = True


class ProductConfig(BaseConfig):
    DEBUG = False
