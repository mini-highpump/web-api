#!/usr/bin/python
#coding: utf-8

from datetime import datetime
from _base import db, config

'''
Favor model mapped to t_favor_list table.
'''

class FavorList(db.Model):
    __tablename__ = "t_favor_list"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uid = db.Column(db.String(64), db.ForeignKey("t_user_info.uid")) 
    sid = db.Column(db.String(64), db.ForeignKey("t_song_info.sid"))
    state = db.Column(db.SmallInteger, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modify_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


    def __init__(self, uid, sid, state):
        self.uid = uid
        self.sid = sid
        self.state = state
