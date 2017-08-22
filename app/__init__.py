#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog  : http://liuyue.club/
# Pw @ 2017-08-03 16:06:48

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import DevConfig

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevConfig)
    db.init_app(app)
    bootstrap.init_app(app)

    from upsync import upsync as upsync_print
    app.register_blueprint(upsync_print)

    return app
