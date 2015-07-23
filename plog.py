from plog import run
from optparse import OptionParser
import os,sys
import signal

def signal_handler(sig, frame):
    pid=os.getpid()
    os.kill(pid, signal.SIGQUIT)

if __name__ == "__main__":


    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = OptionParser() 
    parser.add_option("-c", "--config", dest="config_filename",
                            help="config file for parse log")

    (options, args) = parser.parse_args()
    
    
    if options.config_filename is None :
        print "config  file is none"
        sys.exit(1)
    else :
        try:
            if not os.path.exists(options.config_filename):
                print "there is not  config_file ,you should creat_cfg first,refer to https://github.com/xluren/Plog"
                sys.exit(1)
            else:
                config_file=options.config_filename
        except:
            print "read config error,check it exists or not,refer to https://github.com/xluren/Plog"
            sys.exit(1)

    run(config_file=config_file,debug=False)
