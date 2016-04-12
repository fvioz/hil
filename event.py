# -*- coding: utf-8 -*-

from threading import Thread
from multiprocessing import Process, Queue, freeze_support, set_start_method

class HilEvent(Thread):
  def __init__(self, component, target, args):
    super(HilEvent, self).__init__()
    self.component = component
    self.target = target
    self.args = args

  def run(self):
    set_start_method('forkserver')
    pr = Process(target=self.target, args=self.args)
    pr.start()
    return pr.join()
