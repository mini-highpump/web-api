#!/usr/bin/python
#coding: utf-8
import urllib2
import urllib
import base64
import redis
import json
import time
import random


def get(url, data={}):
    seq = [key+"="+value for key, value in data.iteritems()]
    new_url = url
    if len(seq) > 0:
        new_url = url + "?" + "&".join(seq)
    return json.loads(urllib2.urlopen(new_url).read())


def post(url, data):
    return json.loads(urllib2.urlopen(url, data=urllib.urlencode(data)).read())


def get_uinfo(uid):
    return base64.standard_b64encode(uid + ":" + str(int(time.time())))


def ASSERT_RET(r):
    assert(r["retcode"] == 0 and r["retmsg"] == "ok")


class ApplicationTest(object):
    def __init__(self):
        self.url = "http://localhost:5000/app/"
        self.authurl = "http://localhost:5000/auth/"
        self.r = redis.Redis("localhost")


    @property
    def uid(self):
        return self._uid


    @property
    def token(self):
        return self._token


    def pack_param(self):
        data = {}
        data["uinfo"] = get_uinfo(self._uid)
        data["token"] = self._token
        return data


    def get_token(self, mode=1):
        if mode == 1:
            r = get(self.url + "get_token")
        else:
            data = self.pack_param()
            r = post(self.url + "get_token", data)
        ASSERT_RET(r)
        self._uid = r["uid"]
        self._token = r["token"]


    def get_auth(self, code):
        data = self.pack_param()
        data["code"] = code
        r = post(self.authurl + "get_step", data)
        print r
        ASSERT_RET(r)


    def choose_mode(self, mode):
        data = self.pack_param()
        data["mode"] = mode
        r = post(self.url+"choose_mode", data)
        ASSERT_RET(r)
        assert(self.r.get("user_mode_" + self._uid) == str(mode))


    def get_play_list(self, speed, sid_list=[]):
        data = self.pack_param()
        data["speed"] = speed
        if len(sid_list) > 0:
            data["songs"] = "|".join(sid_list)
        r = post(self.url + "get_play_list", data)
        ASSERT_RET(r)
        print r
        return r


    def switch_song(self, speed, sid):
        data = self.pack_param()
        data["speed"] = speed
        data["sid"] = sid
        r = post(self.url + "switch_song", data)
        ASSERT_RET(r)
        print r
        return r


    def toggle_like(self, sid):
        data = self.pack_param()
        data["sid"] = sid
        r = post(self.url + "toggle_like", data)
        ASSERT_RET(r)


    def get_history_list(self):
        data = self.pack_param()
        r = post(self.url + "get_history_list", data)
        ASSERT_RET(r)
        print r
        return r


class PoolTest(object):
    def __init__(self, uid, token):
        self.uid = uid
        self.token = token

    
    def download(self, url):
        response = urllib2.urlopen(url)
        f = open("tmp.mp4", "w")
        f.write(response.read())


def runTest():
    print "Test Begin..."
    app = ApplicationTest()
    # login
    app.get_token()
    app.get_token(2)
    app.get_auth("12345566")
    # choose_mode
    app.choose_mode(1)
    # get_play_list
    r = app.get_play_list(150)
    if len(r["lists"]) <= 0:
        raise Exception("Playlist is empty.")
    sid = r["lists"][0]["sid"]
    url = r["lists"][0]["url"]
    
    # download song
    pool = PoolTest(app.uid, app.token)
    pool.download(url)

    # switch_song
    r = app.switch_song(190, sid)
    if len(r["lists"]) <= 0:
        raise Exception("Playlist is empty.")
    sid_list = [item["sid"] for item in r["lists"]]

    r = app.get_play_list(160, sid_list)

    i = int(random.random() * len(sid_list))
    j = int(random.random() * len(sid_list))

    print "[%d]%s" % (i, sid_list[i])
    print "[%d]%s" % (j, sid_list[j])

    for sid in sid_list:
        app.toggle_like(sid)

    # like
    # app.toggle_like(sid_list[i])
    # unlike
    # app.toggle_like(sid_list[j])

    # get_history_list
    app.get_history_list()
    print "Test End..."


if __name__ == "__main__":
    runTest()
