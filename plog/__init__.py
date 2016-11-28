from plog.common.base import read_conf
import threading
from Queue import Queue 
import time,datetime
import logging,logging.handlers,signal
from setproctitle import setproctitle
import sys,os

class redict_stderr(object):
   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level

   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

def init_log_conf(log_config_option):
    logging_format = log_config_option["logging_format"]
    logging_level = log_config_option["logging_level"]
    logging_filename = log_config_option["logging_filename"]

    logging.basicConfig(
        format = logging_format,
        level = int(logging_level),
        filename = logging_filename
    )

    stdout_logger = logging.getLogger('STDOUT')
    std_out = redict_stderr(stdout_logger, int(logging_level))
    sys.stdout = std_out

    stderr_logger = logging.getLogger('STDERR')
    std_err = redict_stderr(stderr_logger, int(logging_level))
    sys.stderr = std_err

    root=logging.getLogger()
    handler = logging.handlers.RotatingFileHandler(
                logging_filename,maxBytes=1024*1024*10,
                backupCount=2)
    root.addHandler(handler)

    logging.info("init log  conf done ")

def consume_queue_timer(sink_controller, sink_dict,dict_queue):

    interval = int(sink_dict["interval"])

    current_time = time.time()
    dealing_time = current_time-current_time%interval

    sleep_time = 1
    while 1:
        current_time = time.time()
        if current_time > dealing_time + interval:
            dealing_time = current_time - current_time % interval
            sink_controller.deal_sink()

        else :
            dict_queue_size = dict_queue.qsize()
            if dict_queue.qsize() > 0:
                dict_item = dict_queue.get()
                sink_controller.calculate_item(item=dict_item)
            else:
                time.sleep(sleep_time)

def run(config_file, logger, debug=False):
    setproctitle("plog worker "+config_file)
    dict_queue = Queue()

    conf_dict = read_conf(config_file=config_file).get_conf_dict()

    # log_config_option = conf_dict["log_config"]
    # init_log_conf(log_config_option=log_config_option)

    source_module_name = conf_dict["source"]["source_module"]
    source_module = __import__("plog.source.%s" % source_module_name,fromlist=["plog.source"])
    source_iter = source_module.source(source_dict=conf_dict["source"]).yield_line()

    channel_module_name = conf_dict["channel"]["channel_module"]
    channel_module = __import__("plog.channel.%s" % channel_module_name,fromlist=["plog.channel"])
    channel_controller = channel_module.channel(channel_dict=conf_dict["channel"],
                                        source_iter=source_iter,
                                        dict_queue=dict_queue)

    sink_module_name = conf_dict["sink"]["sink_module"]
    sink_module = __import__("plog.sink.%s" % sink_module_name,fromlist=["plog.sink"])

    sink_controller = sink_module.sink(sink_dict=conf_dict["sink"], logger=logger)

    producer = threading.Thread(
        target=channel_controller.parse_line
    )

    consumer = threading.Thread(
        target=consume_queue_timer,
        args=(sink_controller,conf_dict["sink"],dict_queue)
    )

    producer.start()
    consumer.start()

    while 1:
        if len(threading.enumerate()) != 3:
            pid = os.getpid()
            os.kill(pid, signal.SIGQUIT)
        else:
            time.sleep(120)
