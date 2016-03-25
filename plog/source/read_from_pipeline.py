from plog.source.base import source_base
import os
import time
import sys

class source(source_base):

    def __init__(self, source_dict):
        self.source_interval = int(source_dict["source_interval"])

    def yield_line(self):
        while 1:
            try:
                #line = raw_input()
                line = sys.stdin.readline()
                if line:
                    yield line
                else:
                    time.sleep(self.source_interval)
            except EOFError:
                pid = os.getpid()
                os.kill(pid, signal.SIGQUIT)
                print "end of the file"
