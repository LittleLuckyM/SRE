#!/bin/bash
count=`ps -ef | grep '$1' |grep -v "grep"|wc -l`
M_IPADDR=`ifconfig eth0|grep "Bcast"|awk '{print $2}'|cut -d: -f 2`
DATE=`date`
EMAIL=email.txt
if [ $count -eq 0 ];then

cat >$EMAIL <<EOF
֪ͨ���ͣ�����

����$1

������ $M_IPADDR

״̬ ������
EOF

        echo "warining"
        mail -s "$M_IPADDR $1 warning" 289501651@qq.com < $EMAIL # >>/dev/null 2>&1  
else
        echo "$1 ok"
fi
