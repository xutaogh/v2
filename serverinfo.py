#! /usr/bin/env python
# -*- coding: utf-8 -*-

import readjson
import urllib2
import base64
import os
import json
# 获取本机IP地址
myip = urllib2.urlopen('http://api.ipify.org').read()
myip = myip.strip()

# 判断传输配置
mystreamnetwork = str(readjson.ConfStreamNetwork)
streamtype = str()
mystream = str()

if readjson.ConfStreamNetwork == "kcp":
    if(readjson.ConfStreamHeader == "utp"):
        mystreamnetwork = "kcp"
        streamtype = "utp"
        mystream = "mKCP 伪装 BT下载流量"
    elif(readjson.ConfStreamHeader == "srtp"):
        mystreamnetwork = "kcp"
        streamtype = "srtp"
        mystream = "mKCP 伪装 FaceTime通话"
    elif(readjson.ConfStreamHeader == "wechat-video"):
        mystreamnetwork = "kcp"
        streamtype = "wechat-video"
        mystream = "mKCP 微信视频流量"
    elif(readjson.ConfStreamHeader == "dtls"):
        mystreamnetwork = "kcp"
        streamtype = "dtls"
        mystream = "mKCP 伪装 数据包传输层安全性协议"
    else:
        mystreamnetwork = "kcp"
        streamtype = "none"
        mystream = "mKCP 无伪装"
elif readjson.ConfStreamNetwork == "h2":
    mystreamnetwork = "h2"
    streamtype = "none"
    mystream = "HTTP/2流量"
elif readjson.ConfStreamNetwork == "ws":
    mystreamnetwork = "ws"
    streamtype = "none"
    mystream = "WebSocket流量"
elif readjson.ConfStreamNetwork == "tcp":
    if(readjson.ConfStreamHeader == "http"):
        mystreamnetwork = "tcp"
        streamtype = "http"
        mystream = "TCP 伪装 HTTP"
    else:
        mystreamnetwork = "tcp"
        streamtype = "none"
        mystream = "TCP 无伪装"


if (readjson.ConfStreamSecurity == "tls"):
    mystreamsecurity = "TLS：开启"
else:
    mystreamsecurity = "TLS：关闭"

# 输出信息
print("服务器IP：%s") % str(myip)
print("主端口：%s") % str(readjson.ConfPort)
print("UUID：%s") % str(readjson.ConfUUID)
print("alter ID: %s") % str(readjson.ConfAlterId)
print("加密方式：%s") % str(readjson.ConfSecurity)
print("传输方式：%s") % str(mystream)
if readjson.ConfigDynPortRange:
    print("动态端口范围:%s") % str(readjson.ConfigDynPortRange)
else:
    print("动态端口:禁止")


# config["host"] = str(readjson.ConfPath)

def GetVmessUrl():
    config = {
        "v": "2",
        "ps": "v2rayN V2.x",
        "add": "",
        "port": "",
        "id": "",
        "aid": "",
        "net": "",
        "type": "none",
        "host": "",
        "path": "",
        "tls": "",
    }
    config["add"] = str(myip)
    config["port"] = str(readjson.ConfPort)
    config["id"] = str(readjson.ConfUUID)
    config["aid"] = str(readjson.ConfAlterId)
    config["net"] = str(mystreamnetwork)
    config["type"] = str(streamtype)

    if (readjson.ConfSecurity == "tls"):
        config["tls"] = "tls"
    base64Str = base64.encodestring(json.dumps(config))
    base64Str = ''.join(base64Str.split())
    vmessurl = "vmess://" + base64Str
    return vmessurl


def GetVmessUrlPepi():
    mystreamnetwork = str(readjson.ConfStreamNetwork)
    base64Str = base64.urlsafe_b64encode(str(readjson.ConfSecurity) + ":" + str(
        readjson.ConfUUID) + "@" + str(myip) + ":" + str(readjson.ConfPort))
    vmessurl = "vmess://" + base64Str + "?obfs=" + str(mystreamnetwork)
    return vmessurl


def GreenShow(string):
    print("\033[32m")
    print("%s") % string
    print("\033[0m")


def GenQRCode(name, string):
    os.system("qrcode -w 200 -o ~/" + name + " " + string)


def ShowQRCode(string):
    os.system("qrcode -w 200 " + string)


print("=====  V2rayN v2.x =====")
GreenShow(GetVmessUrl())
GenQRCode("config_v2rayN.png", GetVmessUrl())

print("=====  Pepi(ios) 1.0.7(87) =====")
GreenShow(GetVmessUrlPepi())
GenQRCode("config_pepi.png", GetVmessUrlPepi())
