#!/usr/bin/python
#coding: utf-8
'''
Music pool
Convert url_id to real sid and return the song
'''
from flask import Blueprint, request, g
from .. import tool


bp = Blueprint("pool", __name__)


@bp.route("/music/<url_id>", methods=["GET"])
@tool.begin
@tool.required_login
@tool.pack_return
def download(url_id):
    # TODO
    pass
