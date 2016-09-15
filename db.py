#!/usr/bin/python
#coding: utf-8
from highpump import app
from highpump.models import db

with app.app_context():
    # db.drop_all()
    db.create_all()
