#!/usr/bin/python
#coding: utf-8

from _base import db, config
from datetime import datetime


'''
Playlist model mapped to t_play_list table
'''

class PlayList(db.Model):
    __tablename__ = "t_play_list"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    uid = db.Column(db.String(64), db.ForeignKey("t_user_info.uid"))
    sid = db.Column(db.String(64), db.ForeignKey("t_song_info.sid"))
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cost_time = db.Column(db.SmallInteger, nullable=False, default=0)


    def __init__(self, uid, sid, cost_time=0):
        self.uid = uid
        self.sid = sid
        self.cost_time = cost_time
