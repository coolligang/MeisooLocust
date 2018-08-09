# -*- coding: utf-8 -*-

from locust import HttpLocust
from gevent import monkey
from tasks.MeisooTasks import MeisooTasks
from restVariable.MeisooVar import MeisooVar
from tool.RfeLibrary import RfeLibrary

monkey.patch_all()


class Lancher(HttpLocust):
    user_id = "82"
    user_name = "liuyanqing"
    password = "888888"
    host_str = "http://betagateway.meitianiot.com:80"

    meisooVar = MeisooVar()
    login_var = meisooVar.LoginVar(user_name, password)
    rfeLib = RfeLibrary()
    rs = rfeLib.reqByDataform(host_str + login_var.getUrl(), login_var.getForm(), login_var.getHeaders())
    token = rfeLib.getValueFromJson(rs, "$.data.auth")
    user_info = {"id": user_id, "phone": "liuyanqing", "code": "888888", "token": token}

    host = "http://10.10.253.8:8080"
    task_set = MeisooTasks
    min_wait = 1000
    max_wait = 5000
