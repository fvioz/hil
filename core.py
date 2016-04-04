# -*- coding: utf-8 -*-
import time
import daemon
import logging
from hil.api import HilApi
from hil.control import HilControl
from hil.component import HilComponent
# from hil.emiter import HilEmiter

class HilCore:
  def __init__(self):
    #self.__api = HilApi(self)
    self.__control = HilControl(self)

  def addComponent(self, component):
    if not issubclass(component, HilComponent):
      raise TypeError("Param must be of type HilComponent")
    self.__control.install(component)

  def start(self):
    print('entro')
    with daemon.DaemonContext():
      while True:
        print("Running")
        time.sleep(5)
