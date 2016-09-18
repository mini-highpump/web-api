#!/usr/bin/python
#coding: utf-8

from _base import db
from datetime import datetime


class UrlMap(db.Model):
    '''
    UrlMap model mapped to t_song_url_map table
    '''
    __tablename__ = "t_song_url_map"
    url_id = db.Column(db.String(128), primary_key=True, nullable=False)
    uid = db.Column(db.String(64), db.ForeignKey("t_user_info.uid"), nullable=False)
    sid = db.Column(db.String(64), db.ForeignKey("t_song_info.sid"), nullable=False)
    key = db.Column(db.String(64), nullable=False)
    expires = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __init__(self, url_id, uid, sid, key, expires=0):
        self.url_id = url_id
        self.uid = uid
        self.sid = sid
        self.key = key
        self.expires = expires
