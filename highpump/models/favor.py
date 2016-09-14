#!/usr/bin/python
#coding: utf-8

from datetime import datetime
from _base import db, config

'''
Favor model mapped to t_favor_list table.
'''
FavorList = db.Table("t_favor_list", 
                db.Column("uid", db.String(32), db.ForeignKey("t_user_info.uid")), 
                db.Column("sid", db.String(32), db.ForeignKey("t_song_info.sid")), 
                db.Column("state", db.ShortInteger, nullable=False), 
                db.Column("create_time", db.DateTime, nullable=False, default=datetime.now()), 
                db.Column("modify_time", db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
            )
