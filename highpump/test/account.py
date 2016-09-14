#!/usr/bin/python
#coding: utf-8
import urllib
import urllib2
import time
import base64
import json
import os

from tools import hash, gettimestamp

def print_status(func):
    def wrapper(self):
        self.func()
        print '{0} is called.'.format(func.__name__)
    return wrapper

class AccountTest(object):
    '''
    Account interface testcase. 
    '''
    # host = 'http://115.29.103.94:4000'
    host = 'http://localhost:5000'
    # host = 'http://www.uniqueguoqi.com:4000'
    # model = 'account'
    def __init__(self, tel, pwd):
        self.tel = tel
        self.pwd = pwd

    def spliceurl(self, model, action):
        return '/'.join([self.host, model, action])

    def genrequest(self, model, action, data, method='GET'):
        if method not in ('GET', 'POST'):
            raise ValueError('Method Error')
        d = urllib.urlencode(data)
        u = self.spliceurl(model, action)
        if method == 'GET':
            return urllib2.Request(u + '?' + d)
        else:
            return urllib2.Request(u, d)

    # @print_status
    def reg(self):
        data = {
                'tel': self.tel, 
                'pwd': base64.encodestring(self.pwd)
            }
        return urllib2.urlopen(self.genrequest('account', 'reg', data, 'POST'))

    # @print_status
    def verify(self):
        v = raw_input('Please input captcha: ')
        dd = int(time.time())
        data = {
                'v': hash(':'.join([v, str(dd)])), 
                'dd': dd
            }
        return urllib2.urlopen(self.genrequest('account', 'verify', data, 'POST'))

    # @print_status
    def u_profile(self):
        v = raw_input('Please input user\'s profile.Use key=value pairs to specify a specified property.Use spaces to seprate words.\n')
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            print tt
            d[tt[0]] = tt[1]
        d['uid'] = self.uid
        dd = int(time.time())
        d['auth'] = hash(':'.join([self.token, str(dd)]))
        d['dd'] = dd
        return urllib2.urlopen(self.genrequest('account', 'profile', d, 'POST'))

    # @print_status
    def new_pwd(self):
        v = raw_input('Please input new pwd: ')
        dd = int(time.time())
        data = {
                'uid': self.uid, 
                'auth': hash(':'.join([self.token, str(dd)])), 
                'dd': dd, 
                'new_pwd': base64.encodestring(v)
            }
        return urllib2.urlopen(self.genrequest('account', 'pwd', data, 'POST'))

    # @print_status
    def info(self):
        v = int(raw_input('Please input a user id'))
        d = {'uid': v}
        return urllib2.urlopen(self.genrequest('account', 'info', d))

    # @print_status
    def login(self):
        dd = int(time.time())
        data = {
                'tel': self.tel, 
                'info': hash(':'.join([self.tel, hash(self.pwd), str(dd)])), 
                'dd': dd
            }
        return urllib2.urlopen(self.genrequest('account', 'login', data, 'POST'))

    def a_release(self):
        v = raw_input('Please input activity\'s info.\n')
        dd = int(time.time())
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            print tt
            d[tt[0]] = tt[1]
        d['uid'] = self.uid
        d['auth'] = hash(':'.join([self.token, str(dd)]))
        d['dd'] = dd
        return urllib2.urlopen(self.genrequest('activity', 'release', d, 'POST'))

    def a_profile(self):
        v = raw_input('Please input activity\'s info.\n')
        dd = int(time.time())
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            print tt
            d[tt[0]] = tt[1]
        d['uid'] = self.uid
        d['auth'] = hash(':'.join([self.token, str(dd)]))
        d['dd'] = dd
        return urllib2.urlopen(self.genrequest('activity', 'profile', d, 'POST'))

    def delete(self):
        v = int(raw_input('Please input aid.\n'))
        dd = int(time.time())
        d = {
            'uid': self.uid, 
            'auth': hash(':'.join([self.token, str(dd)])), 
            'dd': dd, 
            'aid': v
        }
        return urllib2.urlopen(self.genrequest('activity', 'delete', d, 'POST'))

    def near(self):
        v = raw_input('Please input longitude and latitude via l=l and b=b.\n')
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            print tt
            d[tt[0]] = float(tt[1])
        return urllib2.urlopen(self.genrequest('activity', 'near', d))

    def a_list(self):
        v = raw_input('Please input start num.\n')
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            print tt
            if tt[0] == 's':
                d[tt[0]] = int(tt[1])
            else:
                d[tt[0]] = float(tt[1])
        dd = int(time.time())
        # d['uid'] = self.uid
        # d['auth'] = hash(':'.join([self.token, str(dd)]))
        # d['dd'] = dd
        return urllib2.urlopen(self.genrequest('activity', 'list', d, 'POST'))

    def search(self):
        v = raw_input('Please input keyword.\n')
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            print tt
            if tt[0] == 'q':
                d[tt[0]] = tt[1]
            else:
                d[tt[0]] = float(tt[1])
        return urllib2.urlopen(self.genrequest('activity', 'search', d))

    def participants(self):
        v = int(raw_input('Please input aid.\n'))
        d = {'aid': v}
        return urllib2.urlopen(self.genrequest('activity', 'participants', d))

    def join(self):
        v = int(raw_input('Please input aid.\n'))
        dd = int(time.time())
        d = {
            'uid': self.uid, 
            'auth': hash(':'.join([self.token, str(dd)])), 
            'dd': dd,
            'aid': v
        }
        return urllib2.urlopen(self.genrequest('activity', 'join', d, 'POST'))

    def voteup(self):
        v = int(raw_input('Please input aid.\n'))
        dd = int(time.time())
        d = {
            'uid': self.uid, 
            'auth': hash(':'.join([self.token, str(dd)])), 
            'dd': dd, 
            'aid': v
        }
        return urllib2.urlopen(self.genrequest('activity', 'voteup', d, 'POST'))

    def r_list(self):
        v = raw_input('Please input aid and start.\n')
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            d[tt[0]] = int(tt[1])
        return urllib2.urlopen(self.genrequest('review', 'list', d))

    def r_release(self):
        v = raw_input('Please input review.\n')
        dd = int(time.time())
        tmp = v.split(' ')
        d = {}
        for t in tmp:
            tt = t.split('=')
            d[tt[0]] = tt[1]
        d['uid'] = self.uid, 
        d['auth'] = hash(':'.join([self.token, str(dd)]))
        d['dd'] = dd
        return urllib2.urlopen(self.genrequest('review', 'release', d, 'POST'))

    def upload(self, img):
        if not os.path.isfile(img):
            return False 
        file, e = os.path.splitext(img)
        f = open(img, 'rb')
        bytes = f.read()
        f.close()
        dd = int(time.time())
        d = {
                'uid': self.uid, 
                'auth': hash(':'.join([self.token, str(dd)])), 
                'dd': dd, 
                'img': base64.encodestring(bytes), 
                'ext': e[1:]
            }
        print e[1:]
        print d['img']
        return urllib2.urlopen(self.genrequest('account', 'avatar', d, 'POST'))


    def test_main(self):
        '''
        Main test function.
        '''
        def assert_response(r):
            print json.dumps(r, indent=4, ensure_ascii=False)
            assert(r['status'] is True and r['message'] == 'OK')
        # r = json.loads(self.reg().read())
        # assert_response(r)
        # r = json.loads(self.verify().read())
        # assert_response(r)
        r = json.loads(self.login().read())
        assert_response(r)
        self.uid = r['result']['Actor']['uid']
        self.token = r['result']['Actor']['token']
        # r = json.loads(self.u_profile().read())
        # print self.token
        # assert_response(r)
        # r = json.loads(self.new_pwd().read())
        # assert_response(r)
        # r = json.loads(self.info().read())
        # assert_response(r)
        # r = json.loads(self.u_profile().read())
        # print self.token
        # assert_response(r)
        # print 'Release.'
        # r = json.loads(self.a_release().read())
        # assert_response(r)
        # print 'Release'
        # r = json.loads(self.a_release().read())
        # assert_response(r)
        # print 'Profile'
        # r = json.loads(self.a_profile().read())
        # assert_response(r)
        # print 'Near'
        # r = json.loads(self.near().read())
        # assert_response(r)
        # print 'Join'
        # r = json.loads(self.join().read())
        # assert_response(r)
        # print 'Voteup'
        # r = json.loads(self.voteup().read())
        # assert_response(r)
        print 'List'
        r = json.loads(self.a_list().read())
        assert_response(r)
        # print 'Participants'
        # r = json.loads(self.participants().read())
        # assert_response(r)
        # print 'Search'
        # r = json.loads(self.search().read())
        # assert_response(r)
        # r = json.loads(self.upload('/home/guoqi/Pictures/background.jpg').read())
        # assert_response(r)

if __name__ == '__main__':
    # a = AccountTest('13667225239', '12345')
    a = AccountTest('13260614509', '123')
    a.test_main()
