# -*- coding: utf-8 -*-

from tool.RfeLibrary import RfeLibrary
from entity.Rest import Rest
from tool.meisooUtil import meisooUtil
import random

class MeisooVar:
    terminalGW = "/api/t/v1/"
    orderGW = "/api/order/v1/"

    def __init__(self):
        self.rfeLib = RfeLibrary()

    def GwRandStrategy(self, url, extra):
        rest = Rest("post", url)
        util = meisooUtil()
        triceId = util.getAnyElementRandom()
        timestamp = self.rfeLib.getTimestampFormat()

        md5_str = self.rfeLib.toMD5(
                extra + "_" + timestamp + "_" + triceId + "_" + url + "_Adhj8dsAScxcsdf72323huc8dfhf")

        header = {"TRACE_ID": triceId, "TIMESTAMP": timestamp, "EXTRA": extra, "SIGN": md5_str}
        rest.setHeaders(header)
        return rest

    def GwTokenStrategy(self, url, token, userId):
        rest = Rest("post", url)
        util = meisooUtil()
        triceId = util.getAnyElementRandom()
        timestamp = self.rfeLib.getTimestampFormat()

        md5_str = self.rfeLib.toMD5(
                userId + "_" + token + "_" + timestamp + "_" + triceId + "_" + url + "_xjaK9as98291Kdsds")

        header = {"TRACE_ID": triceId, "TIMESTAMP": timestamp, "TOKEN": token, "USER_ID": userId, "SIGN": md5_str}
        rest.setHeaders(header)
        return rest

    def LoginVar(self, phone, codePSW):
        url = self.terminalGW + "terminal/app/login"
        extra = "phone=" + phone + "&code=" + codePSW
        rest = self.GwRandStrategy(url,extra)
        form = {"phone": phone, "code": codePSW}
        rest.setForm(form)
        return rest

    def getListAnyElement(self,list):
        """
        随机获取list中某个元素\n
        :param list:需要获取元素存在的list\n
        :return:list中的某个随机元素
        """
        #获取list长度
        length = len(list)
        #随机获取list长度以内的下标
        x = random.randint(0, length-1)
        #获取list的随机下标的元素
        e = list[x]
        return e


