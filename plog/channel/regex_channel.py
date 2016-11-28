from plog.channel.base import channel_base
import os
import time
import re

class channel(channel_base):

    def __init__(self,channel_dict,source_iter,dict_queue):
        self.channel_regex      = channel_dict["channel_filter_regex"]
        self.source_iter        = source_iter
        self.dict_queue         = dict_queue
        self.pattern            = self.gen_pattern()

    def gen_pattern(self):
        return re.compile(self.channel_regex)
    
    def parse_line(self):
        for line in self.source_iter:
            try:
                match=self.pattern.match(line)
                if match:
                    self.dict_queue.put(match.groupdict())
                else :
                    pass
            except:
                print "log"
