# -*- coding: utf-8 -*-

import time
import daemon
import logging

from hil.control import HilControl
from hil.component import HilComponent

class HilCore:
  def __init__(self):
    #self.__api = HilApi(self)
    self.__control = HilControl(self)

  def addComponent(self, component):
    if not issubclass(component, HilComponent):
      raise TypeError("Param must be of type HilComponent")
    self.__control.install(component)

  def trigger(self, component, target, args):
    self.__control.trigger(component, target, args)

  def start(self):
    # with daemon.DaemonContext():
    while True:
      time.sleep(1)
