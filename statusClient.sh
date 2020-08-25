#!/usr/bin/env bash

installClient() {
  echo -e "请输入服务端IP：\n"
  read -e -p "IP: " serverIp
  echo -e "请输入服务端端口：\n"
  read -e -p "PORT: " port
  echo -e "请输入节点用户名：\n"
  read -e -p "USERNAME: " username
  echo -e "请输入节点密码：\n"
  read -e -p "PASSWORD: " password

  wget --no-check-certificate -qO client-linux.py "https://raw.githubusercontent.com/Etnous/ServerStatus/master/client-linux.py"
  chmod 755 client-linux.py
  mv client-linux.py /home/
  cat > /lib/systemd/system/statusClient.service <<-EOF
[Unit]
Description=StatusClient
After=network.target

[Service]
Restart=always
Type=simple
ExecStart=/usr/bin/python /home/client-linux.py SERVER=$serverIp PORT=$port USER=$username PASSWORD=$password

[Install]
WantedBy=multi-user.target
EOF
  systemctl daemon-reload
  systemctl enable statusClient
  systemctl restart statusClient
  echo -e "客户端安装完成！"
}

main(){
  clear
  echo -e "
======ServerStatus Client======
 1. 安装客户端
 2. 重启客户端
 3. 卸载客户端
==============================="
  read -e -p "请输入数字[1-3]:" selectNum
  case $selectNum in
  1)
    installClient
    ;;
  2)
    systemctl restart statusClient
    echo "重启完成！"
    ;;
  3)
    systemctl stop statusClient
    systemctl disable statusClient
    rm -rf /home/client-linux.py
    rm -rf /lib/systemd/system/statusClient.service
    echo "卸载完成！"
    ;;
  *)
    echo "请输入正确的数字" && exit 1
    ;;
  esac
  
}

main
