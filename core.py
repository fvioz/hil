# -*- coding: utf-8 -*-

import os
import sys
import time


from hil import routes
from hil.log import logger
from hil.api import HilApi
from hil.config import HilConfig
from hil.control import HilControl

class HilCore:

  VERSION = '0.0.1'

  def __init__(self, apps, context):
    """"""
    try:
      self.config = HilConfig(apps, context)
    except Exception as e:
      logger.critical(str(e))
      raise sys.exit(-1)

    self.api = HilApi(routes)
    self.control = HilControl(self.config)

  def __del__(self):
    """"""
    self.stop()

  def start(self):
    """"""
    self.__welcomeMessage()
    self.running = True
    while self.running:
      try:
        if not self.api.running:
          self.api.start(self.control)
        time.sleep(0.1)
      except (KeyboardInterrupt, SystemExit):
        self.stop()

    self.__exitMessage()

  def restart(self):
    pass

  def stop(self):
    """"""
    try:
      self.api.stop()
    except:
      pass
    self.running = False

  def __welcomeMessage(self):
    """Prints shutdown message."""
    print("=> Booting Hil version {0}".format(self.VERSION))

  def __exitMessage(self):
    """Prints shutdown message."""
    print("\n=> Shutdown the server\n=> Bye")
