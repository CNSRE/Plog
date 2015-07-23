#!/bin/bash 
string_start='ww2.baidu.cn 120.192.83.910   3 TCP_HIT  '
string_end='"GET /58.jpg HTTP/0.0" 200 4099 "http://1223.com/p" "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36" "-"'
start_time=`date "+%s"`
file="plog_demo.log"
touch ${file}
i=0
while :
do
    now_time=`date "+%s"`
    output="${string_start}  [`date "+%d/%b/%Y:%H:%M:%S"` +0800] ${string_end}"
    echo $output >> ${file}
    inteval=$(( $now_time-$start_time ))
    let i=${i}+1
    sleep 1
    if [ ${inteval} -gt 300 ]
    then 
        break
    fi 
done
mv ${file} ${file}.bak
touch ${file}
while :
do
    now_time=`date "+%s"`
    output="${string_start}  [`date "+%d/%b/%Y:%H:%M:%S"` +0800] ${string_end}"
    echo $output >> ${file}
    inteval=$(( $now_time-$start_time ))
    let i=$i+1
    sleep 1
    if [ ${inteval} -gt 300 ]
    then 
        break
    fi 
done
