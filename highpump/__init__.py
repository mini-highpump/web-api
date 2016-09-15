#!/usr/bin/python
#coding: utf-8
from flask import Flask
from config import DevelopmentConfig
from counter import create_counter, get_counter


def init_app():
    '''
    Initialize the app
    return an object of Flask
    '''
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    init_db(app)
    init_blueprint(app)
    init_errorhandlers(app)
    init_counter()
    return app


def init_db(app):
    '''
    Initialize the datebase.
    '''
    from models import db
    db.init_app(app)


def init_blueprint(app):
    '''
    Initialize blueprints
    '''
    from controllers import application, pool
    app.register_blueprint(application.bp, url_prefix='/application')
    app.register_blueprint(pool.bp, url_prefix='/pool')


def init_errorhandlers(app):
    import json
    from error import ThrownError, InternalError

    @app.errorhandler(ThrownError)
    def thrownerror(e):
        r = {
                'status': False, 
                'message': e.err, 
                'result': ''
            }
        return json.dumps(r)

    @app.errorhandler(500)
    @app.errorhandler(InternalError)
    def internalerror(e):
        r = {
                'status': False, 
                'message': 'Internal Error', 
                'result': ''
            }
        return json.dumps(r)


def init_counter():
    create_counter("uid", 23)
    create_counter("sid", 11)
    create_counter("url_id", 10)


app = init_app()
