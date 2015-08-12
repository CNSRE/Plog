Plog
====

Plog 是 "Parse Log" 的缩写,是一套处理日志流的框架，日志流格式可以是Apache，nginx等常规意义的日志格式，也可以是自定义格式

受[FlumeNG](http://flume.apache.org/)的启发，我把整个工程分成了三个部分:**source**,**channel** ,**sink**,已经完成了主体的共有的可以抽象出来的功能，比如线程的同步互斥，消息的生产消费，处理时间间隔的控制，还有一些简单的source,channel and sink函数


下面是一个简单的配置文件:
<pre>
[source]
#定义读取数据的模块名
source_module=file_source
#定义源文件
source_file=./test/plog_demo.log
#定义读取文件的时间间隔，单位s
source_interval=5

[channel]
#定义解析数据的模块名
channel_module=regrex_channel
#如是正则，定义正则规则
channel_filter_regex=([\w\d.\s,]{0,})\s([0-9.]+)\s(?P<response_time>\d+|-)\s(\w+)\s\[([^\[\]]+)\s\+\d+\]\s"((?:[^"]|\")+)"\s(?P<response_code>\d{3})\s(\d+|-)\s"((?:[^"]|\")+|-)"\s"(.+|-)"\s"((?:[^"]|\")+)"\s"(.+|-)"$

[sink]
#定义发送数据的时间间隔
interval=60
#定义计算与发送的模块名
sink_module=zabbix_sink
sink_service=cacheL2
#定义需要的key
sink_zabbix_monitor_keys=200,300,400,500
#定义发送给zabbix写数据的文件
sink_zabbix_send_file=/tmp/zabbix_send_info
#定义发送zabbix sender路径
sink_zabbix_sender=/usr/bin/zabbix_sender
#定义zabbix的配置文件
sink_zabbix_conf=/etc/zabbix/zabbix_agentd.conf

[log_config]
#定义输出log的格式，级别，路径等，方便调试程序。
logging_format=%(asctime)s %(filename)s [funcname:%(funcName)s] [line:%(lineno)d] %(levelname)s %(message)s
logging_level=20
logging_filename=/tmp/plog.log
</pre>


使用了[ConfigParse](https://docs.python.org/2/library/configparser.html)来解析配置文件


#### source部分的设计思路

在这一部分，我们需要处理的是数据流的来源，他可能是file，可能是socket，可能是管道，但是我不关注你的数据来源格式是什么样的，因为我无法满足这些需要各式各样的数据来源需求，而你的需要是什么样的，你最清楚，那么你只要写一个**source**的插件就可以了,名字随意你定，你需要的是把你写的那个插件的名字，写到**plog.conf**里面，默认有读取文件的file_source模块，读取管道的read_from_pipeline模块，可以直接使用。

<pre>
source_module=self-define-script-name
</pre>
自定义source的具体实现，参看source module下的**plog/source/youself_define_source.py**

#### channel部分
在这个部分,主要是对数据流的处理，你同样需要写一个 Python的脚本，名字随意你定，但是你需要写到 **plog.conf** 中，默认有解析python正则的模块可以直接使用，类似下方:
<pre>
channel_module=filter_log
</pre>
同样的你需要实现的channel可以参见 **plog/channel/youself_define_channel.py**

**grok_channel**

这里实现了另外的一个grok channel模块，底层调用的是pygrok库，如果你对logstash比较熟悉，那么你应该可以比较灵活的使用Plog的grok channel。但在此之前你要确保你的系统已经安装了regex模块。在$Plog_HOME/conf/plog.conf中指定使用grok channel模块，并添加相应日志解析的grok pattern。比如像下面这样：

<pre>
channel_module=grok_channel
channel_filter_grok=%{HOSTNAME}\s%{DATA}\s%{NUMBER:response_time}\s%{WORD}\s\[.*\]\s\".*\"\s%{WORD:response_code}
</pre>

#### sink 部分
在这个部分，你同样需要写一个Python脚本，他的名字同样取决于你的个人喜好，你需要的是把你写的那个插件的名字写到**plog.conf**，例如下方:
<pre>
sink_module=cacheL2get_monitor
</pre>
同样的你需要完成的脚本可以参见**plog/sink/youself_define_sink.py**


#### 如何跑一个测试
下面的测试是读取一个本地本件，解析，计算自己要想的结果发送到zabbix监控系统。
<pre>
1.git clone https://github.com/SinaMSRE/Plog.git

2.cd ./Plog/test 

3.sh gen_log.sh & 

4.cd .. && python plog.py -c conf/plog.conf

5.you will see a file**/tmp/zabbix_send_info_test123**,its contents like followings:
[xxxx@test Plog]$ cat /tmp/zabbix_send_info_test123
xxxx test123_300 0.000000
xxxx test123_200 59.000000
xxxx test123_500 0.000000
xxxx test123_400 0.000000
</pre>

