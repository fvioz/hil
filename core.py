# -*- coding: utf-8 -*-

import time

from hil import routes
from hil.api import HilApi
from hil.control import HilControl
from hil.component import HilComponent

class HilCore:
  def __init__(self):
    self.running = False
    self.__api = HilApi(self, routes)
    self.__control = HilControl(self)

  def __del__(self):
    self.stop()

  def addComponent(self, component):
    if not issubclass(component, HilComponent):
      raise TypeError("Param must be of type HilComponent")
    self.__control.install(component)

  def start(self):
    self.running = True
    self.__api.start()
    while self.running:
      try:
        time.sleep(0.1)
      except (KeyboardInterrupt, SystemExit):
        self.stop()

  def stop(self):
    self.__api.stop()
    self.__control.stop()
    self.running = False

  def trigger(self, component, target, args = None):
    self.__control.trigger(component, target, args)
