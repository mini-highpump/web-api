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
from ..models.song import Song
from ..config import BaseConfig
from comm import normal_recommend


bp = Blueprint("app", __name__)


@bp.route("/get_token", methods=["GET", "POST"])
@tool.begin
@tool.pack_return
def get_uid():
    if request.method == "GET":
        # 新用户第一次访问, 分配uid
        uid = tool.get_uid(request.remote_addr)
        u = User(uid)
    else:
        tool.filter(["uinfo", "token"])(lambda : True)()
        tool.required_login(lambda : True)()
        u = g.user
    u.key = tool.get_key()
    u.expires = int(time.time()) + 7200
    db.session.add(u)
    db.session.commit()
    gr.set("user_start_time_" + u.uid, datetime.now(), 7200)
    g.result["uid"] = u.uid
    g.result["token"] = tool.get_token(u.key, u.uid, u.expires)


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
    if g.args.has_key("songs"):
        sid_list = g.args["songs"].split("|")
        do_set_play_list(g.user.uid, sid_list)
    do_get_song_list(g.user.uid, g.args["speed"])


@bp.route("/switch_song", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "sid", "speed"])
@tool.required_login
@tool.pack_return
def switch_song():
    do_set_play_list(g.user.uid, [g.args["sid"]])
    do_get_song_list(g.user.uid, g.args["speed"])


@bp.route("/toggle_like", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "sid"])
@tool.required_login
@tool.pack_return
def toggle_like():
    f = FavorList.query.filter(FavorList.uid == g.user.uid and FavorList.sid == g.args["sid"]).all()
    if len(f) > 1:
        raise InternalError(-10003, "Affected rows more than 1.")
    elif len(f) == 0:
        f = FavorList(g.user.uid, g.args["sid"], 2)
    else:
        f = f[0]
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
    play_list = PlayList.query.filter(PlayList.start_time > start_time).filter(PlayList.end_time < str(end_time)).all()
    g.result["total_num"] = len(play_list)
    g.result["lists"] = []
    for item in play_list:
        song = Song.query.get(item.sid)
        t = song.to_dict()
        t["time_cost"] = item.cost_time
        f = FavorList.query.filter(FavorList.uid == g.user.uid, FavorList.sid == item.sid).first()
        print f
        if f is not None and f.state == 2:
            t["is_favorite"] = "1"
        else:
            t["is_favorite"] = "0"
        g.result["lists"].append(t)


'''
Real get song list.
'''
def do_get_song_list(uid, speed):
    uid = g.user.uid
    mode = int(gr.get("user_mode_" + uid))
    songs = normal_recommend(uid, float(g.args["speed"]), mode)
    g.result["total_num"] = len(songs)
    g.result["lists"] = []
    for s in songs:
        print s.sid
        t = s.to_dict()
        key = tool.get_key()
        expires = int(time.time()) + 600
        url_id = tool.get_urlid(key, uid, s.sid, expires, 600)
        t["url"] = BaseConfig.HOST + "/pool/music/" + url_id 
        item = FavorList.query.filter(FavorList.sid == s.sid, FavorList.uid == uid).first()
        print item
        if item is not None and item.state == 2:
            t["is_favorite"] = "1"
        else:
            t["is_favorite"] = "0"

        g.result["lists"].append(t)

        urlmap = UrlMap(url_id, uid, s.sid, key, expires)
        db.session.add(urlmap)
        db.session.commit()

        playlist = PlayList(uid, s.sid)
        db.session.add(playlist)
        db.session.commit()


'''
Set play list.
'''
def do_set_play_list(uid, sid_list):
    for sid in sid_list:
        play_list = PlayList.query.filter(PlayList.uid == uid and PlayList.sid == sid) \
                                    .order_by(PlayList.start_time.desc()).first()
        if play_list is None:
            continue
        if play_list.end_time is None:
            continue
        curtime = datetime.now()
        play_list.end_time = curtime
        play_list.cost_time = (curtime - play_list.start_time).seconds
        db.session.add(play_list)
    db.session.commit()
