# -*- coding: utf-8 -*-

import os
import sys
import time
import multiprocessing

from hil import routes
from hil.log import logger
from hil.api import HILApi
from hil.config import HILConfig
from hil.control import HILControl
from hil.decorator import HILNonOverridable, non_overridable

class HILCore:

  __metaclass__ = HILNonOverridable

  VERSION = '0.0.1'

  def __init__(self, apps, context):
    """Contructor the object"""
    self.api_conn, self.control_api_conn = multiprocessing.Pipe()
    self.config_conn, self.control_config_conn = multiprocessing.Pipe()

    try:
      self.config = HILConfig(self.config_conn, apps, context)
    except Exception as e:
      logger.critical(str(e))
      raise sys.exit(-1)

    self.api = HILApi(routes, self.control_api_conn)
    self.control = HILControl(self.config, self.api_conn, self.control_config_conn)

  def __del__(self):
    """Destroys the object"""
    self.stop()

  def start(self):
    """Starts the core server"""
    try:
      self._welcomeMessage()
      self.running = True
      while self.running:
        if not self.api.running:
          self.api.start()
        if not self.control.running:
          self.control.start()
        time.sleep(.1)
    except (KeyboardInterrupt, SystemExit):
      self.stop()

    self._exitMessage()

  def restart(self):
    """Restarts the core server"""
    self.stop()
    self.start()

  def stop(self):
    """Stops the core server"""
    try:
      self.api.stop()
      self.control.stop()
    except:
      pass
    self.running = False

  @non_overridable
  def _welcomeMessage(self):
    """Prints shutdown message."""
    print("=> Booting HIL version {0}".format(self.VERSION))

  @non_overridable
  def _exitMessage(self):
    """Prints shutdown message."""
    print("\n=> Shutdown the server\n=> Bye")
