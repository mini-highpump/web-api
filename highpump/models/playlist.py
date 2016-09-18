#!/usr/bin/python
#coding: utf-8

from _base import db, config
from datetime import datetime


'''
Playlist model mapped to t_play_list table
'''

class PlayList(db.Model):
    __tablename__ = "t_play_list"
    id = db.Column("id", primary_key=True, nullable=False)
    uid = db.Column("uid", db.String(64), db.ForeignKey("t_user_info.uid"))
    sid = db.Column("sid", db.String(64), db.ForeignKey("t_song_info.sid"))
    start_time = db.Column("start_time", db.DateTime, nullable=False, default=datetime.now)
    end_time = db.Column("end_time", db.DateTime, nullable=True)
    cost_time = db.Column("cost_time", db.Integer, nullable=False, default=0)


    def __init__(self, uid, sid):
        self.uid = uid
        self.sid = sid
