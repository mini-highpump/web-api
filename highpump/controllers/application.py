#!/usr/bin/python
#coding: utf-8
'''
Main application
Provide api which is called by frontend.
'''
import time
from datetime import datetime
from flask import Blueprint, request, g
from .. import tool, gr
from ..models import db
from ..models.user import User
from ..models.favor import FavorList
from ..models.urlmap import UrlMap
from ..models.playlist import PlayList
from comm import normal_recommend


bp = Blueprint("app", __name__)


@bp.route("/get_uid", methods=["GET", "POST"])
@tool.begin
@tool.pack_return
def get_uid():
    if request.method == "GET":
        # 新用户第一次访问, 分配uid
        uid = tool.get_uid()
        u = User(uid)
    else:
        tool.filter(lambda x : x, ["uinfo", "token"])()
        tool.required_login(lambda x : x)()
        u = g.user
    u.key = tool.get_key()
    u.expires = int(time.time()) + 7200
    db.session.add(u)
    db.session.commit()
    gr.set("user_start_time_" + u.id, datetime.now(), 7200)
    g.result["uid"] = u.id
    g.result["token"] = get_token(u.key, u.uid, u.expires)


@bp.route("/choose_mode", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "mode"])
@tool.required_login
@tool.pack_return
def choose_mode():
    gr.set("user_mode_" + g.user.uid, g.args["mode"])


@bp.route("/get_play_list", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "speed"])
@tool.required_login
@tool.pack_return
def get_play_list():
    do_get_song_list()


@bp.route("/switch_song", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "sid", "speed"])
@tool.required_login
@tool.pack_return
def switch_song():
    play_list = PlayList.query.filter(PlayList.uid == g.user.uid and PlayList.sid == g.args["sid"]).last()
    if play_list.end_time is not None:
        raise ThrownError(-20001, "Parameters error.")
    curtime = datetime.now()
    play_list.end_time = curtime
    play_list.cost_time = (curtime - play_list.start_time).second
    db.session.add(play_list)
    db.session.commit()
    do_get_song_list()


@bp.route("/toggle_like", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "sid"])
@tool.required_login
@tool.pack_return
def toggle_like():
    f = FavorList.query.filter(FavorList.uid == g.user.uid and FavorList.sid == g.args["sid"]).all()
    if len(f) > 1:
        raise InternalError(-10003, "Affected rows more than 1.")
    if f.state == 1:
        f.state = 2
    else:
        f.state = 1
    db.session.add(f)
    db.session.commit()


@bp.route("/get_history_list", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token"])
@tool.required_login
@tool.pack_return
def get_history_list():
    end_time = datetime.now()
    start_time = gr.get("user_start_time_" + g.user.uid)
    play_list = PlayList.query.filter(PlayList.start_time > start_time and PlayList.end_time < str(end_time)).all()
    g.result["total_num"] = len(play_list)
    i = 0
    for item in play_list:
        song = Song.query.get(item.sid)
        index = "row_" + str(i)
        g.result[index] = dict(song)
        g.result[index]["time_cost"] = item.cost_time
        if s.favor_users.query.filter(User.uid == uid).first() is None:
            g.result[index]["is_favorite"] = "0"
        else:
            g.result[index]["is_favorite"] = "1"
        i += 1


'''
Real get song list.
'''
def do_get_song_list(uid, speed):
    uid = g.user.uid
    mode = gr.get("user_mode_" + uid)
    songs = normal_recommend(uid, float(g.args["speed"]), mode)
    g.result["total_num"] = len(songs)
    i = 0
    for s in songs:
        index = "row_" + str(i)
        g.result[index] = {}
        g.result[index] = dict(s)
        key = tool.get_key()
        expires = int(time.time()) + 600
        url_id = tool.get_urlid(key, uid, s.sid, expires, 600)
        g.result[index]["url"] = config.HOST + "/pool/" + url_id 
        if s.favor_users.query.filter(User.uid == uid).first() is None:
            g.result[index]["is_favorite"] = "0"
        else:
            g.result[index]["is_favorite"] = "1"

        urlmap = UrlMap(url_id, uid, s.sid, key, expires)
        db.session.add(urlmap)
        i += 1
    db.session.commit()
