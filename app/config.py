#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog  : http://liuyue.club/
# Pw @ 2017-08-03 16:06:48

import os
import datetime
import etcd
basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig():
    DEBUG = True
    SECRET_KEY = "1yIuTUJzH1JUrui5a2a0bsur8efMg9m3"
    SQLALCHEMY_DATABASE_URI = 'mysql://liuyue:password@localhost:3306/upsync?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # CLIENT = "asdf"
    CLIENT = etcd.Client(host="10.37.253.72", port=2379)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=10)
