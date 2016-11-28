from plog.source.base import source_base
from plog.source.base import source_base
import os
import time
class source(source_base):

    def __init__(self, source_dict):
        self.source_interval = int(source_dict["source_interval"])
        self.source_file = source_dict["source_file"]
        self.file_inode = 0

    def get_file_inode(self):
        try:
            file_inode = os.stat(self.source_file).st_ino
        except:
            try :
                file_inode = os.stat(self.source_file).st_ino
            except:
                file_inode = 0
                print "here"
        return file_inode

    def read_file(self):

        tmp=""
        with open(self.source_file) as file_handle:
            file_handle.seek(0,2)
            while 1:
                line_list = file_handle.readlines()
                if not line_list:
                    file_inode_now = self.get_file_inode()
                    if file_inode_now != self.file_inode:
                        yield 1,"inode change"
                    else:
                        time.sleep(self.source_interval)
                else:
                    for line in line_list:
                        if not line.endswith("\n"):
                            tmp = line
                        else:
                            line = tmp+line
                            tmp = ""
                            yield 0,line
    def yield_line(self):
        while 1:
            self.file_inode = self.get_file_inode()
            for status,line in self.read_file():
                if status == 1:
                    time.sleep(0.5)
                    break
                else:
                    yield line
