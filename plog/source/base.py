import abc
class source_base(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def yield_line(self):
        pass
