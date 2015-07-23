import ConfigParser

class read_conf(object):
    def __init__(self,config_file):
        self.config_file=config_file
    def get_conf_dict(self):
        conf=ConfigParser.RawConfigParser()
        conf.read(self.config_file)
        option_dict={}
        secs=conf.sections()
        for sec in secs:
            option_dict[sec]={}
            for option in  conf.options(sec):
                key=option
                value=conf.get(sec,key)
                option_dict[sec][key]=value
        return option_dict
