from plog.channel.base import channel_base
from plog.channel.base import channel_base
from pygrok import pygrok
import os
import time

class channel(channel_base):

    def __init__(self,channel_dict,source_iter,dict_queue):
        self.channel_grok       = channel_dict["channel_filter_grok"]
        self.source_iter        = source_iter
        self.dict_queue         = dict_queue

    def parse_line(self):
        '''            
        the grok channel
        '''
        for line in self.source_iter:
            try:
                match=pygrok.grok_match(line,self.channel_grok)
                if match:
                    print("testlog is match! this log is:" + str(match) )
                    print("parse:%s" %match)
                    self.dict_queue.put(match)
                else:
                    pass
            except:
                print "log"
