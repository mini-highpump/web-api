#!/usr/bin/python
#coding: utf-8
'''
Music pool
Convert url_id to real sid and return the song
'''
import urllib2
import json
from flask import Blueprint, request, g
from .. import tool, gr
from ..error import ThrownError, InternalError

URL_ACCESS_TOKEN = "https://api.weixin.qq.com/sns/oauth2/access_token"
URL_REFRESH_TOKEN = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
URL_GET_STEP = "https://api.weixin.qq.com/hardware/snstransfer/bracelet/getstep"

APPID = "wxda065e7b6fcfa601"
APP_SECRET = "3fd784596deca10931b6ca8add80c14b"

WX_TOKEN_KEY_PREFIX = "wx_token_"


bp = Blueprint("auth", __name__)


@bp.route("/get_step", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "code"])
@tool.required_login
@tool.pack_return
def get_step():
    if gr.hexists(WX_TOKEN_KEY_PREFIX + g.user.uid, "access_token"):
        acc_token = gr.hget(WX_TOKEN_KEY_PREFIX + g.user.uid, "access_token")
    else:
        acc_token, re_token = access_token(g.user.uid, g.args["code"])
    print "Access Token:%s" % acc_token
    r = getstep(g.user.uid, acc_token)
    g.result["step"] = r["step"]
    g.result["timestamp"] = r["timestamp"]


def access_token(uid, code):
    data = {
            "appid": APPID, 
            "secret": APP_SECRET, 
            "code": code,
            "grant_type": "authorization_code"
        }
    r = tool.get(URL_ACCESS_TOKEN, data)
    print r
    if r.has_key("errcode"):
        if r["errcode"] == 42001:
            raise ThrownError(-20006, "access_token超时, 需要重新授权")
        raise ThrownError(r["errcode"], r["errmsg"])
    # 写入redis缓存
    d = {
            "access_token": r["access_token"], 
            "refresh_token": r["refresh_token"]
        }
    gr.hmset(WX_TOKEN_KEY_PREFIX + uid, d)
    return (r["access_token"], r["refresh_token"])


def refresh_token(uid, refresh_token):
    data = {
            "appid": APPID, 
            "grant_type": "refresh_token", 
            "refresh_token": refresh_token
        }
    r = tool.get(URL_REFRESH_TOKEN, data)
    print r
    if r.has_key("errcode"):
        if r["errcode"] == 42002:
            raise ThrownError(-20006, "refresh_token超时, 需要重新授权")
        raise ThrownError(r["errcode"], r["errmsg"])
    d = {
            "access_token": r["access_token"], 
            "refresh_token": r["refresh_token"]
        }
    gr.hmset(WX_TOKEN_KEY_PREFIX + uid, d)
    return (r["access_token"], r["refresh_token"])


def getstep(uid, access_token):
    data = {
            "access_token": access_token
        }
    r = tool.get(URL_GET_STEP, data)
    print r
    if r.has_key("errcode") and r["errcode"] != 0:
        if r["errcode"] == 42001: # access_token超时
            refresh_token = gr.hget(WX_TOKEN_KEY_PREFIX + uid, "refresh_token")
            acc_token, re_token = refresh_token(uid, refresh_token)
            r = tool.get(URL_GET_STEP, data)
            print r
            # 重试一次
            if r["errcode"] != 0:
		if r.has_key("msg"):
		    msg = r["msg"]
                else:
		    msg = r["errmsg"]
                raise ThrownError(r["errcode"], msg)
        else:
	    if r.has_key("msg"):
	        msg = r["msg"]
	    else:
	        msg = r["errmsg"]
            raise ThrownError(r["errcode"], msg)
    return r
