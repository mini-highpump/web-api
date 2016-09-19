#!/usr/bin/python
#coding: utf-8
'''
Music pool
Convert url_id to real sid and return the song
'''
from flask import Blueprint, request, g, Response, make_response, stream_with_context
from .. import tool
from ..error import ThrownError
from ..models.urlmap import UrlMap


bp = Blueprint("pool", __name__)


@bp.route("/music/<url_id>", methods=["GET"])
@tool.begin
def download(url_id):
    print "UrlId:%s" % url_id
    urlmap = UrlMap.query.get(url_id)
    if urlmap is None:
        raise ThrownError(-20001, "Parameters error.")
    print urlmap.sid
    filepath = "/data/song/" + urlmap.sid + ".mp4"
    print filepath
    try:
        f = file(filepath, "r")
    except IOError:
        raise ThrownError(-20005, "File not exists.")
    return Response(f.read(), mimetype="audio/mpeg")
