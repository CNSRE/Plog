from plog.sink.base import sink_base
from plog.sink.base import sink_base
import os
import time

#the class name must be sink
class sink(sink_base):

    def __init__(self,sink_dict):

        """
           here is you sink_dict
           it contains the key:value
           you write in the config file
        """

        self.service            = sink_dict['service']
        self.send_dict          = {}
        
        self.zabbix_send_file   = "_".join((self.service,sink_dict['zabbix_send_file']))
        self.zabbix_sender      = sink_dict['zabbix_sender']
        self.zabbix_conf        = sink_dict['zabbix_conf']

        self.dealed_total       = 0
    
    def calculate_item(self,item):
        
        """
            you calculate method here
            you must implement the method
            a simple example below
        """

        response_code   = item['response_code']
        response_time   = int(item['response_time'])
        
        try:
            request_url=item["request_url"].split()[1].split('/')[1]
        except:
            request_url="others"

        response_code       = response_code[0:1]+"xx"     
        
        total_count         = "count"
        avgrt               = "avgrt"
        total_time          = "total_time"
        

        url_count           = request_url+"_count"
        url_total_time      = request_url+"_total_time"
        url_avgrt           = request_url+"_avgrt"
        url_response_code   = "_".join((url,response_code))

        sum_key_list=[response_code,response_time,url_count,
                        url_total_time,url_response_code]
        avg_key_list=[avgrt,url_avgrt]

        for key in sum_key_list:
            if key not in self.send_dict:
                self.send_dict[key]=0
            else :
                self.send_dict[key]+=1
        for key in avg_key_list:
            if key.find("_")!=-1:
                key_prefix=key[0:0:-len("_avgrt")]
                self.send_dict[key]=self.send_dict[key_prefix+"_total_time"]/self.send_dict[key_prefix+"_count"]
            else:
                self.send_dict[key]=self.send_dict["total_time"]/self.send_dict["count"]
    
    def deal_sink(self):
        """
            you deal method here
            you must implement the method
            a simple example below
        """
        import platform
        hostname=platform.uname()[1]
        with open(self.sink_zabbix_send_file,"w") as file_handle:
            for key in  self.send_dict:
                info="%s %s_%s %f\n" % (hostname,service,str(key),send_dict[key])
                file_handle.write(info)
                send_dict[key]=0

        cmd="%s -c %s -i %s" % (self.zabbix_sender,self.zabbix_conf,self.zabbix_send_file)
        status,output=commands.getstatusoutput(cmd)
    def you_self_define_func(self):
        """
            here is you self define method
            if you need one 
        """
        pass
