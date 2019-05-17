#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# 检查是否为Root
[ $(id -u) != "0" ] && { echo "Error: You must be root to run this script"; exit 1; }

# 检查系统信息
if [ -f /etc/redhat-release ];then
        OS='CentOS'
    elif [ ! -z "`cat /etc/issue | grep bian`" ];then
        OS='Debian'
    elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
        OS='Ubuntu'
    else
        echo "Not support OS, Please reinstall OS and retry!"
        exit 1
fi

# 禁用SELinux
if [ -s /etc/selinux/config ] && grep 'SELINUX=enforcing' /etc/selinux/config; then
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
    setenforce 0
fi

# 安装依赖
if [[ ${OS} == 'CentOS' ]];then
    curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
	yum install curl wget unzip git ntp ntpdate lrzsz python socat nodejs -y
    npm install -g qrcode
else
    curl -sL https://deb.nodesource.com/setup_8.x | bash -
	apt-get update
	apt-get install curl unzip git ntp wget ntpdate python socat lrzsz nodejs -y
    npm install -g qrcode
fi

# 安装 acme.sh 以自动获取SSL证书
curl  https://get.acme.sh | sh

# 克隆V2ray.fun项目
cd /usr/local/
rm -R v2ray.fun
git clone https://github.com/xutaogh/v2

# 安装V2ray主程序
bash <(curl -L -s https://install.direct/go.sh)

# 配置V2ray初始环境
ln -sf /usr/local/v2/v2ray /usr/local/bin
chmod +x /usr/bin/v2ray
chmod +x /usr/local/bin/v2ray
rm -rf /etc/v2ray/config.json
cp /usr/local/v2/json_template/server.json /etc/v2ray/config.json
let PORT=$RANDOM+10000
UUID=$(cat /proc/sys/kernel/random/uuid)
sed -i "s/cc4f8d5b-967b-4557-a4b6-bde92965bc27/${UUID}/g" /etc/v2ray/config.json
sed -i "s/12345/${PORT}/g" "/etc/v2ray/config.json"
python /usr/local/v2/genclient.py
python /usr/local/v2/openport.py
service v2ray restart

# auto open port after start
# append a new line
cat /etc/rc.local | grep openport.py
if [[ $? -ne 0 ]]; then
cat>>/etc/rc.local<<EOF
python /usr/local/v2/openport.py
EOF
chmod a+x /etc/rc.local
fi


clear

echo "V2 安装成功！"
echo "输入 v2ray 回车即可使用"
