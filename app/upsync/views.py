#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog  : http://liuyue.club/
# Pw @ 2017-08-03 16:32:11

import os
import json
from . import upsync
from flask import current_app, render_template, request, redirect, url_for


@upsync.route("/")
def display_upstream():
    client = current_app.config.get("CLIENT")
    keys = client.get("/upstreams/")
    return render_template("upstreams.html", keys=keys)


@upsync.route("/list/")
def list_upstreams():
    client = current_app.config.get("CLIENT")
    key = request.args.get("key")
    keys = client.get(key)
    return render_template("list_upstream.html", keys=keys, key=os.path.split(key))


@upsync.route("/update/")
def update_upstreams():
    client = current_app.config.get("CLIENT")
    key = request.args.get("key")
    action = request.args.get("action")
    data = {}

    upstreamServer = client.get(key)
    if upstreamServer.value:
        data = json.loads(upstreamServer.value)
    data["status"] = action
    client.write(key, json.dumps(data))

    return redirect(url_for(".list_upstreams", key=os.path.split(key)[0]))