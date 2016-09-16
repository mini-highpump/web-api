#!/usr/bin/python
#coding: utf-8
import random
from .. import gr
from ..models import db
from ..models.song import Song
from ..error import InternalError


def normal_recommend(uid, speed, mode):
    vA = gr.lrange("user_result_" + uid, 0, -1)
    vB = Song.query.filter(compute_by_mode(mode)(speed, Song.bpm)).all()
    result = [item for item in vB if item.sid in vA]
    if len(result) > 3:
        i = int(random.random() * len(result))
        j = int(random.random() * len(result))
        k = int(random.random() * len(result))
        return [result[i], result[j], result[k]]
    return result


def special_recommend(uid, mode):
    vA = gr.lrange("user_result_" + uid, 0, -1)
    if mode == 3:
        vB = Song.query.filter(Song.length < 150 and Song.length > 50).all()
    else:
        vB = Song.query.filter(Song.length < 250 and Song.length > 150).all()
    result = [item for item in vB if item.sid in vA]
    if len(result) > 3:
        i = int(random.random() * len(result))
        j = int(random.random() * len(result))
        k = int(random.random() * len(result))
        return [result[i], result[j], result[k]]
    return result


def compute_by_mode(mode):
    if mode == 1:
        def wrapper(speed, bpm):
            return speed >= (bpm - 10) and speed < (bpm + 10)
    elif mode == 2:
        def wrapper(speed, bpm):
            return speed >= bpm and speed < (bpm + 20)
    return wrapper
