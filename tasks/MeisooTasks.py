# -*- coding: utf-8 -*-

from locust import TaskSet, task
from restVariable.MeisooVar import MeisooVar
from tool.RfeLibrary import RfeLibrary
from tool.meisooUtil import meisooUtil
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class MeisooTasks(TaskSet):
    host = "http://betagateway.meitianiot.com:80"
    payNo = ""
    parkingNo = ""

    @task(1)
    def excecutePayBalance(self):
        self.prePay()
        phone = "13983435205"
        payNo = self.payNo
        token = self.locust.user_info["token"]
        userId = self.locust.user_info["id"]

        # 余额支付，这里的phone是指绑定停车车牌号的用户的手机号
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "common/executeMoneyPay"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"phone": phone, "payNo": payNo}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())
        try:
            # 判断缴费是否成功，成功则会返回channelOrder字段
            channelOrder = rfeLib.getValueFromJson(rs, "$.data.channelOrder")
        except Exception, e:
            raise "Fail -> phone:" + phone + "  payNo:" + payNo
        else:
            # 出场
            self.refundAndOut(self.parkingNo, self.locust.user_info["token"], self.locust.user_info["id"], phone)
            print "Out parkgingNo:" + self.parkingNo + "    channelOrder:" + channelOrder

    def excecutePayAli(self, payNo, token, userId):
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "common/executeMoneyPay"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"payChannel": "1", "payNo": payNo}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())

    def excecutePayWeChat(self, payNo, token, userId):
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "common/executeMoneyPay"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"payChannel": "2", "payNo": payNo}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())

    def prePay(self):
        user = self.locust.user_info
        # 获取空闲车位
        parkingNo = self.getParkingNo(user["token"], user["id"])
        parkingNo = parkingNo["parkItemName"]
        print "In paringNo:" + parkingNo
        # 车辆入场,获取订单号
        orderNo, parkingNo = self.posCarIn(parkingNo, user["token"], user["id"])
        # 绑定车辆和车牌
        orderNo, parkingNo, plateNo = self.posBindPlateNo(parkingNo, user["token"], user["id"], orderNo)
        # 创建付费订单
        payNo, parkingNo = self.createPreOrder(orderNo, parkingNo, plateNo, user["token"], user["id"])
        # 付费,出场,参数传递
        self.payNo = payNo
        self.parkingNo = parkingNo

    def getParkingNo(self, token, userId):
        meisooVar = MeisooVar()
        url = meisooVar.terminalGW + "terminal/app/list"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"parkId": "14"}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())
        parkingNoList = rfeLib.getValueFromJson(rs, "$.data.list")
        msUtil = meisooUtil()
        freeParkingNoList = msUtil.getListElementWithNoKey('parkingState', parkingNoList)
        parkingNo = meisooVar.getListAnyElement(freeParkingNoList)
        return parkingNo

    def posCarIn(self, parkingNo, token, userId):
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "terminal/carIn"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"parkingNo": parkingNo}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())
        orderNo = rfeLib.getValueFromJson(rs, "$.data.orderNo")
        return orderNo, parkingNo

    def posBindPlateNo(self, parkingNo, token, userId, orderNo):
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "terminal/bindPlateNo"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        # 这里要调整，车牌号应该是随机的
        plateNo = "渝ABC520"
        form = {"orderNo": orderNo, "plateNo": plateNo}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())
        result = rfeLib.getValueFromJson(rs, "$.flag")
        if result:
            return orderNo, parkingNo, plateNo

    def createPreOrder(self, orderNo, parkingNo, plateNo, token, userId):
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "parkOut/createOrder"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"orderNo": orderNo, "plateNo": plateNo, "parkingNo": parkingNo, "duration": int(1)}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())
        payNo = rfeLib.getValueFromJson(rs, "$.data.payNo")
        return payNo, parkingNo

    def refundAndOut(self, parkingNo, token, userId, phone):
        meisooVar = MeisooVar()
        url = meisooVar.orderGW + "terminal/pay/refundAndOut"
        rest = meisooVar.GwTokenStrategy(url, token, userId)
        form = {"parkItemName": parkingNo, "phone": phone}
        rest.setForm(form)
        rfeLib = RfeLibrary()
        rs = rfeLib.reqByDataform(self.host + rest.getUrl(), rest.getForm(), rest.getHeaders())
        return rs
