#!/usr/bin/python
#coding: utf-8

from _base import db, config
from datetime import datetime


'''
Playlist model mapped to t_play_list table
'''
PlayList = db.Table("t_play_list", 
                db.Column("uid", db.String(32), db.ForeignKey("t_user_info.uid")), 
                db.Column("sid", db.String(32), db.ForeignKey("t_song_info.sid")),
                db.Column("start_time", db.DateTime, nullable=False, default=datetime.now()), 
                db.Column("end_time", db.DateTime, nullable=True),
                db.Column("cost_time", db.Integer, nullable=False, default=0)
            )
