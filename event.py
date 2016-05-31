# -*- coding: utf-8 -*-

from threading import Thread
from multiprocessing import Process, Queue, freeze_support, set_start_method
from concurrent.futures import ProcessPoolExecutor

class HilEvent(Thread):
  def __init__(self, component, target, args):
    super(HilEvent, self).__init__()
    self.component = component
    self.target = target
    self.args = args
    self.pool = ProcessPoolExecutor(3)

  def run(self):
    set_start_method('forkserver')
    pr = Process(target=self.target, args=self.args)
    pr.start()
    return pr.join()
