#! /usr/bin/env python
# -*- coding: utf-8 -*-
import readjson
import writejson
from utils import is_number

# 读取配置文件信息
mystreamnetwork = str(readjson.ConfStreamNetwork)
if readjson.ConfStreamNetwork == "kcp":
    if(readjson.ConfStreamHeader == "kcp srtp"):
        mystreamnetwork = "mKCP 伪装 FaceTime通话"
    elif(readjson.ConfStreamHeader == "kcp utp"):
        mystreamnetwork = "mKCP 伪装 BT下载流量"
    elif(readjson.ConfStreamHeader == "kcp wechat-video"):
        mystreamnetwork = "mKCP 伪装 微信视频流量"
    elif(readjson.ConfStreamHeader == "kcp dtls"):
        mystreamnetwork = "mKCP 伪装 数据包传输层安全性协议"
    else:
        mystreamnetwork = "mKCP 无伪装"
elif readjson.ConfStreamNetwork == "http":
    mystreamnetwork = "TCP 伪装 HTTP"
elif readjson.ConfStreamNetwork == "ws":
    mystreamnetwork = "WebSocket流量"
elif readjson.ConfStreamNetwork == "h2":
    mystreamnetwork = "HTTP/2流量"
else:
    mystreamnetwork = "TCP 无伪装"

# 显示当前配置
print("当前传输方式为：%s") % mystreamnetwork

# 选择新的传输方式
print("请选择新的传输方式：")
print("1.TCP 无伪装")
print("2.TCP 伪装 HTTP")
print("3.WebSocket流量")
print("4.mKCP 无伪装")
print("5.mKCP 伪装 FaceTime通话")
print("6.mKCP 伪装 BT下载流量")
print("7.mKCP 伪装 微信视频流量")
print("8.mKCP 伪装 数据包传输层安全性协议")
print("9.HTTP/2流量")

newstreamnetwork = raw_input()

if (not is_number(newstreamnetwork)):
    print("请输入数字！")
    exit
else:
    if not (newstreamnetwork > 0 and newstreamnetwork < 8):

        if(newstreamnetwork == "1"):
            writejson.WriteStreamNetwork("tcp", "none")
        elif(newstreamnetwork == "2"):
            print("请输入你想要为伪装的域名（!! 不 要 http!!）：")
            host = raw_input()
            writejson.WriteStreamNetwork("tcp", str(host))
        elif(newstreamnetwork == "3"):
            print("请输入你的服务器绑定域名（!! 不 要 http!!）：")
            host = raw_input()
            writejson.WriteStreamNetwork("ws", str(host))
        elif(newstreamnetwork == "4"):
            writejson.WriteStreamNetwork("mkcp", "none")
        elif(newstreamnetwork == "5"):
            writejson.WriteStreamNetwork("mkcp", "kcp srtp")
        elif(newstreamnetwork == "6"):
            writejson.WriteStreamNetwork("mkcp", "kcp utp")
        elif(newstreamnetwork == "7"):
            writejson.WriteStreamNetwork("mkcp", "kcp wechat-video")
        elif(newstreamnetwork == "8"):
            writejson.WriteStreamNetwork("mkcp", "kcp dtls")
        elif(newstreamnetwork == "9"):
            writejson.WriteStreamNetwork("h2","none")

    else:
        print("请输入有效数字！")
        exit
