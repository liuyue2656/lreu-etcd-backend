#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog  : http://liuyue.club/
# Pw @ 2017-08-03 16:32:16


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Required, IPAddress

class addService(FlaskForm):
    service = StringField(u"服务名称", validators=[Required()])
    submit = SubmitField(u"提交")


class addServer(FlaskForm):
    ip = StringField(u"IP地址", validators=[Required(), IPAddress()])
    port = IntegerField(u"端口号", validators=[Required()])
    status = SelectField(u"状态", choices=[("up", "up"), ("backup", "backup"), ("down", "down")])
    submit = SubmitField(u"提交")


class deleteServer(FlaskForm):
    ip = StringField(u"IP地址", validators=[Required(), IPAddress()])
    port = IntegerField(u"端口号", validators=[Required()])
    submit = SubmitField(u"提交")