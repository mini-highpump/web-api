#!/usr/bin/python
#coding: utf-8

from datetime import datetime
from _base import db
from favor import FavorList


class User(db.Model):
    '''
    User model, mapped to t_user_info table.
    '''
    __tablename__ = "t_user_info"
    uid = db.Column(db.String(64), primary_key=True, nullable=False)
    key = db.Column(db.String(32), nullable=False)
    openid = db.Column(db.String(64), nullable=False, unique=True, default="")
    expires = db.Column(db.Integer, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_refresh_time = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    favor_songs = db.relationship("t_song_info", backref=db.backref("favor_users", lazy="select"), lazy="select", secondary=FavorList)

    def __init__(self, uid, key="", openid="", expires=0):
        self.uid = uid
        self.key = key
        self.openid = openid
        self.expires = expires

    def dump(self):
        return {
                "uid": self.uid, 
                "openid": self.openid
                }
