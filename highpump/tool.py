#!/usr/bin/python
#coding: utf-8
'''
Ubility functions.
'''
from hashlib import md5
import json
import random
import string
import time
import socket
import base64
import struct
import os
import urllib
import urllib2
from Crypto.Cipher import AES
from error import InternalError, ThrownError
from counter import get_counter


def hash(string):
    return md5(string).hexdigest()


def aes_en(key, data):
    obj = AES.new(key, AES.MODE_CFB, '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15')
    return obj.encrypt(data)


def aes_de(key, en_data):
    obj = AES.new(key, AES.MODE_CFB, '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15')
    return obj.decrypt(data)


def get_shuffle_seq(n, r):
    '''
    Generate a shuffle sequence of n length from a list r.
    '''
    seq = []
    for i in xrange(n):
        seq.append(random.choice(r))
    random.shuffle(seq)
    return "".join(seq)


def ip2int(ip):
    return struct.unpack("!I", socket.inet_aton("10.10.64.128"))[0]


def get_uid(client_ip):
    '''
    Get a unique uid.
    Note: this function must be called before a create_counter function call.
    '''
    seq = []
    # get client_ip
    seq.append(str(ip2int(client_ip)))
    # get timestamp
    seq.append(str(int(time.time())))
    # get shuffle sequence
    seq.append(get_shuffle_seq(40 - len(seq[0]) - len(seq[1]), string.digits))
    # get counter counts
    seq.append(str(get_counter("uid").count()))
    result = "".join(seq)
    sum = 0
    for i in xrange(63):
        sum += int(result[i]) * (i + 1)
    return str(sum % 7) + result


def get_sid(filehash):
    '''
    Get a unique sid.
    Note: this function must be called before a create_counter function call.
    '''
    seq = ["s", filehash]
    ts = str(int(time.time()))
    seq.append(get_shuffle_seq(20 - len(ts), string.digits))
    seq.append(ts)
    seq.append(str(get_counter("sid").count()))
    return "".join(seq)


def get_key():
    '''
    Get key.
    '''
    return get_shuffle_seq(32, string.ascii_letters + string.digits + "_-")


def get_urlid(key, uid, sid, expires, valid_length):
    '''
    Get a unique url id
    Note: this function must be called before a create_counter function call.
    '''
    seq = [hash(uid + sid), str(expires), str(valid_length)]
    seq.append(get_shuffle_seq(32 - len(seq[1]) - len(seq[2]), string.ascii_letters + string.digits))
    seq.append(str(get_counter("url_id").count()))
    return (base64.b64encode(
                aes_en(key, "".join(seq)), "y_"
            ))


def get_token(key, uid, expires):
    '''
    Get a token.
    token = md5(aes_en(key, uid+":"+expires))
    '''
    print key, uid, expires
    return hash(aes_en(key, ":".join([uid, str(expires)])))


def begin(func):
    '''
    Begin a request handler.
    '''
    from functools import wraps
    from flask import g
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            g.result = {}
            return func(*args, **kwargs)
        except InternalError, ThrownError:
            raise
        except: # catch other exception
            raise
            # raise InternalError(-10000, "Unknown error.")
    return wrapper


def filter(t):
    '''
    Filter parameters which are essential.
    '''
    def real_decorator(func):
        from functools import wraps
        from flask import g, request
        @wraps(func)
        def wrapper(*args, **kwargs):
            print request.form
            for i in t:
                if not request.form.has_key(i):
                    raise ThrownError(-20001, "Parameters error.")
            g.args = request.form # capture request parameters
            return func(*args, **kwargs)
        return wrapper
    return real_decorator


def pack_return(func):
    '''
    Pack normal return value and output.
    Excute after func.
    '''
    from functools import wraps
    from flask import g
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        g.result["retcode"] = 0
        g.result["retmsg"] = "ok"
        return json.dumps(g.result)
    return wrapper


def required_login(func):
    from flask import g, request
    from functools import wraps
    from models.user import User
    @wraps(func)
    def wrapper(*args, **kwargs):
        uid, ts = base64.standard_b64decode(g.args["uinfo"]).split(":")
        print ts, int(time.time())
        diff = int(time.time()) - int(ts)
        if diff > 12000 or diff < -10:
            raise ThrownError(-20002, "Request timeout.")
        u = User.query.get(uid)
        if u is None:
            raise ThrownError(-20003, "User does\'t exist.")
        if g.args["token"] != get_token(u.key, u.uid, u.expires):
            raise ThrownError(-20004, "Error token.") 
        if u.expires <= int(time.time()):
            raise ThrownError(-20005, "Token timeout. Please refresh it.")
        g.user = u
        g.token = g.args["token"]
        return func(*args, **kwargs)
    return wrapper


def wrap_url(base_uri, **kwargs):
    if kwargs == {}:
        return base_uri
    kwargs.sort()
    r = ["=".join([str(key), str(value)]) for key,value in kwargs.iteritems()]
    return base_uri + "?" + "&".join(r)
    

def get(url, data = {}, type=1):
    '''
    @param type  1-json, 2-binary
    '''
    url = wrap_url(url, **data)
    print url
    try:
        response = urllib2.urlopen(url, timeout=5)
        if type == 1:
            return json.loads(response.read())
        else:
            return response
    except:
        raise InternalError(-10004, "Network connect failed.")
