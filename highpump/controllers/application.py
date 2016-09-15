#!/usr/bin/python
#coding: utf-8
'''
Main application
Provide api which is called by frontend.
'''
import time
from flask import Blueprint, request, g
from .. import tool
from ..models import db
from ..models.user import User
from ..models.favor import FavorList


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
    g.result["uid"] = u.id
    g.result["token"] = get_token(u.key, u.uid, u.expires)


@bp.route("/choose_mode", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "mode"])
@tool.required_login
@tool.pack_return
def choose_mode():
    # TODO
    pass


@bp.route("/get_play_list", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "speed"])
@tool.required_login
@tool.pack_return
def get_play_list():
    pass


@bp.route("/switch_song", methods=["POST"])
@tool.begin
@tool.filter(["uinfo", "token", "sid", "speed"])
@tool.required_login
@tool.pack_return
def switch_song():
    # TODO
    pass


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
    # TODO
    pass
