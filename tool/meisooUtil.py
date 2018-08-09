#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 14:58
# @Author  : chenyx
# @Site    : 
# @File    : GeoUtil.py
# @Software: PyCharm

import random
import sys
import urllib

class meisooUtil:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'

    def __init__(self):
        pass

    def getListAnyElement(self,*list):
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

    def getAnyElementNotInList(self, num=8,*list):
        """
        随机获取的值不属于list\n
        :param *list 被查询的list\n
        :return: ranEle  不属于list的随机获取的值
        """
        #调用随机获取num位字符串方法
        ranEle = self.getAnyElementRandom(num)
        #获取list长度
        size = len(list)
        #获取list最后一个元素
        lastListEle = list[size-1]
        #循环list，如果list中有值与随机获取的num位字符串相等，
        #则调用本方法继续生成一个随机字符串，再循环同lsit里的元素比较
        #直到找出不属于list的值
        for ele in list:
            if ranEle == ele:
                self.getAnyElementNotInList(list)
            elif ele == lastListEle and ranEle != ele:
                break
        return ranEle

    def getAnyElementRandom(self,num=8):
        """
        随机获取num位字符串\n
        :param num 需要获取的字符串长度\n
        :return: num位字符串
        """
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        #循环num-1次
        for i in range(num):
            sa.append(random.choice(seed))
            res = ''.join(sa)
        return res

    def getAnyElementRandomNotNumber(self,num=8):
        """
        随机获取num位非数字符串\n
        :param num 需要获取的字符串长度\n
        :return: num位字符串
        """
        seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        #循环num-1次
        for i in range(num):
            sa.append(random.choice(seed))
            res = ''.join(sa)
        return res

    def getAnyIntRandom(self,min,max):
        """
        获取随机整数\n
        :param min 最小值\n
        :param max 最大值\n
        :return: 随机整数
        """
        res = random.randint(min, max);
        return res


    def getSubString(self,str,indexBegin,indexEnd=None):
        """
        获取截取的字符串\n
        ex:str = 'abcd'\n
           indexBegin = 1\n
           indexEnd = 3\n
           结果：res = bc\n
        :return: string
        """
        if indexEnd != "":
            res = str[indexBegin : indexEnd]
        else:
            res = str[indexBegin : ]
        return res

    def getRexIndexInString(self,str,beFindedStr):
        """
        查询str在beFindedStr中第一次（从左边算起）出现的下标\n
        ex:str = 'abcd'\n
           beFindedStr = '123abcd456'\n
           结果：res = 3\n
        :return: string
        """
        if str != "" and beFindedStr != "":
            res = beFindedStr.index(str)
        else:
            res = -1
        return res

    def getKeyValueInList(self,key,list):
        """
        对元素为map类型的列表，对每个元素中指定的某个key所对应的value进行重新组成list返回\n
        ex:list = [{name = '张三',psw = 123},{name = '李四',psw = 325},{name = '王五',psw = 666}]\n
           key = name\n
           结果：[{'张三'},{'李四'},{'王五'}]\n
        :return: list
        """
        listN = []
        for ele in list:
            dictN = dict(ele)
            valN = dictN.get(key)
            listN.append(valN)
        return listN

    def formatListElement(self, parttern,colNum, list):
        """
        将二维列表中的每个元素进行类型转换\n
        ((1L, u'SaaS'), (2L, u'\u554a\u554a\u554a'), (3L, u'\u6309\u65f6'))\n
        :param parttern: 需要被转换成的类型\n
        :param colNum: 需要被转换list\n
        (1L, u'SaaS')下标只有0，1\n
        :param list: 需要转换的list\n
        :return: 转换后的list
        """
        listN = []
        for ele in list:
            if parttern == 'int':
                listN.append(int(ele[colNum]))
            elif parttern == 'long':
                listN.append(long(ele[colNum]))
            else:
                listN.append(str(ele[colNum]))
        return listN

    def isContain(self,str,res1,res2,type,listStr):
        """
        当包含某字符串时，返回需要的值\n
        :param listStr: 被包含的子字符串list\n
        :param str: 被判断的字符串\n
        :param type: 包含类型\n
                    1.全部包含：listStr中的值全部被包含返回res1，否则返回res2\n
                    2.部分包含: listStr中的值只要一个被包含返回res1，否则返回res2\n
        :param res1: 满足包含条件时返回值\n
        :param res2: 不满足包含条件时返回值\n
        :return: res1/res2\n
        """
        print('传入参数：listStr = ',listStr)
        listStr = list(listStr)
        print('将listStr转为list类型之后：listStr = ',listStr)
        res = res1
        if type == 1:
            for str1 in listStr:
                if str1 not in str:
                    # print('res2 = ', res2)
                    return res2
        elif type == 2:
            for str1 in listStr:
                print("str1=",str1)
                if str1 not in str:
                    res = res2
                else:
                    # print('res1 = ', res1)
                    return res1
        # print('res = ',res)
        return res

    def getRemainString(self,index,str):
        """
        获取去掉某一元素后的字符串\n
        ex:str = 'abcd'\n
           index = 2\n
           结果：res = abd\n
        :return: string
        """
        length = len(str)
        if index == 0:
            res = str[1:length]
        elif index == length-1:
            res = str[0:index]
        else:
            res1 = str[0:index]
            res2 = str[index+1:length]
            res = res1+res2
        return res

    def getRandomProvince(self):
        """
        获取随机省份简称字符串\n
        :return: string
        """
        listX = []
        listX.append('京')
        listX.append('渝')
        listX.append('津')
        listX.append('冀')
        listX.append('晋')
        listX.append('蒙')
        listX.append('辽')
        listX.append('吉')
        listX.append('黑')
        listX.append('沪')
        listX.append('苏')
        listX.append('浙')
        listX.append('皖')
        listX.append('闽')
        listX.append('赣')
        listX.append('鲁')
        listX.append('豫')
        listX.append('鄂')
        listX.append('湘')
        listX.append('粤')
        listX.append('桂')
        listX.append('琼')
        listX.append('川')
        listX.append('黔')
        listX.append('滇')
        listX.append('藏')
        listX.append('陕')
        listX.append('甘')
        listX.append('青')
        listX.append('宁')
        listX.append('新')
        listX.append('港')
        listX.append('澳')
        listX.append('台')
        res = listX[random.randint(0,len(listX)-1)]
        return res

    def getAnyElementRandomJustLetter(self,num=8):
        """
        随机获取num位大写字母字符串\n
        :param num 需要获取的字符串长度\n
        :return: num位字符串
        """
        seed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sa = []
        #循环num-1次
        for i in range(num):
            sa.append(random.choice(seed))
            res = ''.join(sa)
        return res

    def getAnyElementRandomJustNumber(self,num=8):
        """
        随机获取num位数字字符串\n
        :param num 需要获取的字符串长度\n
        :return: num位字符串
        """
        seed = "1234567890"
        sa = []
        #循环num-1次
        for i in range(num):
            sa.append(random.choice(seed))
            res = ''.join(sa)
        return res

    def transUrlUtf8(self,str):
        """
        将Unicode字符串转换为URL的UTF-8编码格式
        :param str:需要进行转换的字符串
        :return:
        """
        newStr = urllib.quote_plus(str.encode('utf8'))
        return newStr

    def getListElementWithNoKey(self, parttern, list):
        """
        判断list中的每个元素是否包含parttern，若不包含则返回此元素\n
        :param parttern: 需要判断是否包含的key\n
        :param list: 需要判断的list\n
        :return: 不包含parttern的元素组成的list
        """
        listN = []
        for ele in list:
            dict(ele)
            if ele.get('parkingState')==None or ele.get('parkingState')==0:
                listN.append(ele)
        return listN

# if __name__=="__main__":
#     test = meisooUtil()
#     list = [{"parkItemName":"011001","parkingState":"0"},{"parkItemName":"011002"},{"parkItemName":"011003"},{"parkItemName":"011004"},{"parkItemName":"011005"},{"parkItemName":"011006"},{"parkItemName":"011007"},{"parkItemName":"011008"},{"parkItemName":"011009"},{"parkItemName":"011010"},{"parkItemName":"011011"}]
#     s = test.getListElementWithNoKey('parkingState',list)
#     print s