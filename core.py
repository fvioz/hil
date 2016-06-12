# -*- coding: utf-8 -*-

import time

from hil import routes
from hil.api import HilApi
from hil.control import HilControl

class HilCore:
  def __init__(self):
    self.running = False
    self.__api = HilApi(self, routes)
    self.__control = HilControl(self)

  def __del__(self):
    self.stop()

  def addComponent(self, klass):
    self.__control.install(klass)

  def start(self):
    self.running = True
    while self.running:
      try:
        if not self.__api.running:
          self.__api.start()
        time.sleep(0.1)
      except (KeyboardInterrupt, SystemExit):
        self.stop()

  def stop(self):
    self.__api.stop()
    self.__control.stop()
    self.running = False

  def trigger(self, klass_namme, target, args):
    self.__control.trigger(klass_namme, target, args)
