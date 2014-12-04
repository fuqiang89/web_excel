# -*- coding: utf-8 -*-
import json
import types
import re

def InitStorage(obj,incfields=[],defaultvalue=""):
    """
    用于初始化storage，补充属性值
    @param obj:需要初始化的storage
    @param incfields:涉及的字段
    @param defaultvalue:默认值
    @return:obj,初始化好的对象
    """
    if incfields:
        for field in incfields:
            if obj.get(field,defaultvalue)==defaultvalue or obj[field]==None:   #不污染原有值
                obj[field]=defaultvalue
    else:
        for field in obj.keys:
            if obj.get(field,defaultvalue)==defaultvalue or obj[field]==None:   #不污染原有值
                obj[field]=defaultvalue
                #初始化好的对象
    return obj
def CopyData_INC(storage1,storage2,incfields=[],default=None):
    """合并属性，将storage2由incfields指定的字段合并入storage1中。
    如属性在2中为None，则不指定
    """
    for field in incfields:
        if storage2.get(field,None)==None:
            storage1[field]=default
        else:
            storage1[field]=storage2[field]
    return storage1
def JsonResult(value):
    """
    返回json编码后的result数据值
    @param value:需要放入result的数据
    @return:{"result":value}json处理后
    """
    vv=json.dumps({'result':value})
    return vv
#判断是否为整数 15
def IsNumber(varObj):
    return type(varObj) is types.IntType
#判断是否为字符串 string
def IsString(varObj):
    return type(varObj) is types.StringType

#判断是否为浮点数 1.324
def IsFloat(varObj):
    return type(varObj) is types.FloatType

#判断是否为字典 {'a1':'1','a2':'2'}
def IsDict(varObj):
    return type(varObj) is types.DictType

#判断是否为tuple [1,2,3]
def IsTuple(varObj):
    return type(varObj) is types.TupleType

#判断是否为List [1,3,4]
def IsList(varObj):
    return type(varObj) is types.ListType

#判断是否为布尔值 True
def IsBoolean(varObj):
    return type(varObj) is types.BooleanType

#判断是否为货币型 1.32
def IsCurrency(varObj):
#数字是否为整数或浮点数
    if IsFloat(varObj) and IsNumber(varObj):
    #数字不能为负数
        if varObj >0:
            return isNumber(currencyObj)
        return False
    return True

#判断某个变量是否为空 x
def IsEmpty(varObj):
    if len(varObj) == 0:
        return True
    return False
#判断变量是否为None None
def IsNone(varObj):
    return type(varObj) is types.NoneType# == "None" or varObj == "none":

#判断是否为日期格式,并且是否符合日历规则 2010-01-31
def IsDate(varObj):
    if len(varObj) == 10:
        rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
        match = re.match( rule , varObj )
        if match:
            return True
        return False
    return False

#判断是否为邮件地址
def IsEmail(varObj):
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match( rule , varObj )
    if match:
        return True
    return False

#判断是否为中文字符串
def IsChineseCharString(varObj):

    for x in varObj:
        if (x >= u"\u4e00" and x<=u"\u9fa5") or (x >= u'\u0041' and x<=u'\u005a') or (x >= u'\u0061' and x<=u'\u007a'):
            continue
    else:
        return False
    return True


#d判断是否为中文字符
def IsChineseChar(varObj):
    if varObj[0] > chr(127):
        return True
    return False

#判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线
def IsLegalAccounts(varObj):
    rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
    match = re.match( rule , varObj )

    if match:
        return True
    return False

#匹配IP地址
def IsIpAddr(varObj):
    rule = '^(?=\d+\.\d+\.\d+\.\d+$)(?:(?:25[0-9]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.?){4}$'
    #rule ='^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$'
    match = re.match( rule , varObj )

    if match:
        return True
    return False

def IsPriIp(obj):
    rule = '^(?=\d+\.\d+\.\d+\.\d+$)(?:(?:25[0-9]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.?){4}$'
    match = re.match( rule , obj )
    if match is None:
        return False
    iplist=obj.split('.')
    #A类
    if int(iplist[0]) == 10:
        return True
    #B类
    if int(iplist[0]) == 172 and 15 < int(iplist[1]) < 32:
        return True
    #C
    if int(iplist[0]) == 192 and  int(iplist[1]) == 168:
        return True
    return False


def IsPubIp(obj):
    rule = '^(?=\d+\.\d+\.\d+\.\d+$)(?:(?:25[0-9]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.?){4}$'
    match = re.match( rule , obj )
    if match is None:
        return False
    if IsPriIp(obj) == True:
        return False

    return True



