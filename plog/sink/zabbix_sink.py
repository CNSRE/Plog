from plog.sink.base import sink_base
from plog.sink.base import sink_base
import os
import time
import commands

class sink(sink_base):

    def __init__(self, sink_dict):

        self.service = sink_dict['sink_service']
        self.send_dict = dict.fromkeys(sink_dict['sink_zabbix_monitor_keys'].split(','),0)
        
        self.zabbix_send_file = "_".join((sink_dict['sink_zabbix_send_file'],self.service))
        self.zabbix_sender = sink_dict['sink_zabbix_sender']
        self.zabbix_conf = sink_dict['sink_zabbix_conf']

        self.dealed_total = 0
    
    def calculate_item(self, item):

        response_code = item['response_code']
        response_time = int(item['response_time'])
        sum_key_list = [response_code]

        #the key like cachel2get_200
        try:
            self.send_dict[str(response_code)]+=1
            print self.send_dict
        except:
            pass
    
    def deal_sink(self):
        import platform
        hostname = platform.uname()[1]
        with open(self.zabbix_send_file,"w") as file_handle:
            for key in  self.send_dict:
                info="%s %s_%s %f\n" % (hostname, self.service, str(key), self.send_dict[key])
                file_handle.write(info)
                self.send_dict[key]=0

        cmd = "%s -c %s -i %s" % (self.zabbix_sender, self.zabbix_conf, self.zabbix_send_file)
        status,output = commands.getstatusoutput(cmd)
