#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# blog  : http://liuyue.club/
# Pw @ 2017-08-03 16:32:11

import os
import json
from . import upsync
from flask import current_app, render_template, request, redirect, url_for, flash
from forms import addServer, addService, deleteServer


@upsync.route("/")
def display_upstream():
    client = current_app.config.get("CLIENT")
    services = client.get("/upstreams/")
    service_list = {}
    for service in services.children:
        service = client.get(service.key)
        service_list[service.key] = []
        for service_child in service.children:
            service_list[service.key].append(service_child.key.split("/")[-1])
        service_list[service.key] = ",".join(service_list[service.key])
    return render_template("upstreams.html", service_list=service_list)


@upsync.route("/guest_index/")
def guest_index():
    client = current_app.config.get("CLIENT")
    services = client.get("/upstreams/")
    service_list = {}
    for service in services.children:
        service = client.get(service.key)
        service_list[service.key] = []
        for service_child in service.children:
            service_list[service.key].append(service_child.key.split("/")[-1])
        service_list[service.key] = ",".join(service_list[service.key])
    return render_template("guest_index.html", service_list=service_list)


@upsync.route("/list/")
def list_upstreams():
    client = current_app.config.get("CLIENT")
    service = request.args.get("service")
    upstreams = client.get(service)
    return render_template("list_upstream.html",
                           upstreams=upstreams,
                           service=os.path.split(service)[1])


@upsync.route("/change_status/")
def change_status():
    client = current_app.config.get("CLIENT")
    upstream = request.args.get("upstream")
    status = request.args.get("status")
    data = {}

    server = client.get(upstream)
    if server.value:
        data = json.loads(server.value)
    data["status"] = status
    client.write(upstream, json.dumps(data))

    return redirect(url_for(".list_upstreams", service=os.path.split(upstream)[0]))


@upsync.route("/change_weight/")
def change_weight():
    client = current_app.config.get("CLIENT")
    upstream = request.args.get("upstream")
    active = request.args.get("active")
    data = {}

    server = client.get(upstream)
    if server.value:
        data = json.loads(server.value)
    if active == "upper":
        data["weight"] = data.get("weight", 1) + 1
    elif active == "lower":
        if data.get("weight", 0) <= 1:
            data["weight"] = 1
        else:
            data["weight"] = data.get("weight", 1) - 1

    client.write(upstream, json.dumps(data))

    return redirect(url_for(".list_upstreams", service=os.path.split(upstream)[0]))


@upsync.route("/add_service/", methods=["get", "post"])
def add_service():
    client = current_app.config.get("CLIENT")
    parent_path = request.args.get("parent_path")

    form = addService()
    if form.validate_on_submit():
        service = os.path.join(parent_path, form.service.data)
        try:
            client.get(service)
        except:
            return redirect(url_for(".add_server", parent_path=service))
        else:
            flash("service is exists.")
        return redirect(url_for(".display_upstream"))

    return render_template("add_service.html", form=form)


@upsync.route("/add_server/", methods=["get", "post"])
def add_server():
    client = current_app.config.get("CLIENT")
    parent_path = request.args.get("parent_path")

    form = addServer()
    if form.validate_on_submit():
        server = ":".join((form.ip.data, str(form.port.data)))
        server_path = os.path.join(parent_path, server)
        data = {"status": form.status.data}
        try:
            client.get(server_path)
        except:
            client.write(server_path, json.dumps(data))
        else:
            flash("server is exists.")
            return redirect(url_for(".display_upstream"))
        return redirect(url_for(".list_upstreams", service=parent_path))
    return render_template("add_server.html", form=form, parent_path=parent_path)


@upsync.route("/delete_server/", methods=["get", "post"])
def delete_server():
    client = current_app.config.get("CLIENT")
    upstream = request.args.get("upstream")
    parent_path, server = os.path.split(upstream)
    form = deleteServer()

    if form.validate_on_submit():
        if server == ":".join((form.ip.data, str(form.port.data))):
            client.delete(upstream)
        else:
            flash("ip or port is not matched.")

        parent = client.get(parent_path)
        if parent.children.next() == parent:
            print "delete parent"
            try:
                client.delete(parent_path, dir=True)
            except:
                pass
            else:
                return redirect(url_for(".display_upstream"))
        return redirect(url_for(".list_upstreams", service=parent_path))
    return render_template("delete_server.html", form=form, upstream=upstream)
