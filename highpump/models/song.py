#!/usr/bin/python
#coding: utf-8

from datetime import datetime
from _base import db


class Song(db.Model):
    '''
    Song model mapped to t_song_info table.
    '''
    __tablename__ = "t_song_info"
    sid = db.Column(db.String(64), primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, default="", server_default="")
    artist = db.Column(db.String(256), nullable=False, default="", server_default="")
    album = db.Column(db.String(256), nullable=False, default="", server_default="")
    genere = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    # Language, 0-Undefined, 1-Chinese, 2-English, 3-Japanese
    language = db.Column(db.SmallInteger, nullable=False, default=0, server_default="0")
    bpm = db.Column(db.Integer, nullable=False, default=0, server_default="0")
    # State, 0-inserted, 1-computing bpm, 2-complete, 3-lost(file not fond)
    state = db.Column(db.Integer, nullable=False, default = 0, server_default="0")
    length = db.Column(db.Integer, nullable=False, default = 0, server_default="0")
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modify_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, sid, bpm, name="", artist="", album="", genere=0, language=0, state=0, length=0):
        self.sid = sid
        self.bpm = bpm
        self.name = name
        self.artist = artist
        self.album = album
        self.genere = genere
        self.language = language
        self.state = state
        self.length = length 


    def to_dict(self):
        return {
                "sid": self.sid, 
                "name": self.name, 
                "artist": self.artist,
                "album": self.album, 
                "genere": self.genere
                }

    
    def dump(self):
        pass
