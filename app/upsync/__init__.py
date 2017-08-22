#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog  : http://liuyue.club/
# Pw @ 2017-08-03 16:32:06

from flask import Blueprint

upsync = Blueprint("upsync", __name__)

from . import views
