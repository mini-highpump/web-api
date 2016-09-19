#!/usr/bin/python
#coding: utf-8
import random
from .. import gr
from ..models import db
from ..models.song import Song
from ..error import InternalError


def normal_recommend(uid, speed, mode):
    speed *= 10
    vA = gr.lrange("user_result_" + uid, 0, -1)
    if mode == 1:
        vB = Song.query.filter(speed >= (Song.bpm - 100), speed < (Song.bpm + 100)).all()
    elif mode == 2:
        vB = Song.query.filter(speed >= Song.bpm, speed < (Song.bpm + 200)).all()
    elif mode == 3 or mode == 4:
        return special_recommend(uid, mode) # 训练模式, 直接返回
    else:
        raise InternalError(-10003, "mode value error.")
    result = [item for item in vB if item.sid in vA]
    if len(result) > 3:
        i = int(random.random() * len(result))
        j = int(random.random() * len(result))
        k = int(random.random() * len(result))
        return [result[i], result[j], result[k]]
    else:
        if len(vB) == 0:
            vB = Song.query.all()
        i = int(random.random() * len(vB))
        print i
        print vB
        result.append(vB[i])
    return result


def special_recommend(uid, mode):
    vA = gr.lrange("user_result_" + uid, 0, -1)
    if mode == 3:
        vB = Song.query.filter(Song.length < 150, Song.length > 50).all()
    else:
        vB = Song.query.filter(Song.length < 250, Song.length > 150).all()
    result = [item for item in vB if item.sid in vA]
    if len(result) > 3:
        i = int(random.random() * len(result))
        j = int(random.random() * len(result))
        k = int(random.random() * len(result))
        return [result[i], result[j], result[k]]
    else:
        if len(vB) == 0:
            vB = Song.query.all()
        i = int(random.random() * len(vB))
        result.append(vB[i])
    return result
