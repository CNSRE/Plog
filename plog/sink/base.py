import abc
class sink_base(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate_item(self):
        pass

    @abc.abstractmethod
    def deal_sink(self):
        pass
