import abc
class channel_base(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse_line(self):
        pass
