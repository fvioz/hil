# -*- coding: utf-8 -*-

import time
import threading
import multiprocessing

from hil.log import logger
from hil.box import HILBox
from hil.config import HILConfig

class HILControl(object):

  def __init__(self, config, api_conn, config_conn):
    self.running = False
    self.config = config
    self.api_conn = api_conn
    self.config_conn = config_conn
    self.current_context = self.config.context(self.config_conn, self.config.contexts)

    multiprocessing.Process(target=self.current_context.call).start()

  def __del__(self):
    self.stop()

  def start(self):
    self.running = True
    while self.running:
      if self.api_conn.poll():
        res = self.api_conn.recv()
        out = self.trigger(res["id"], res["participation"], res["role"], res["callback"], res["timeout"])
        self.api_conn.send(out)
      time.sleep(.1)

  def stop(self):
    self.running = False

  def trigger(self, id, participation, role, callback, timeout):
    """Launchs the current process"""
    if self._participationAllowed(participation) == True:
      action_name = self.config.getAction(participation, role)

      if action_name == None:
        logger.info("[#{}] The request did not have any action".format(id))
        return False
      else:
        actions = self._getActionModules(action_name)
        box = HILBox(id, participation, role, actions, callback, timeout)
        t = threading.Thread(target=box.run, args=())
        t.setDaemon(True)
        t.start()
        logger.info("[#{}] Actions {} launched".format(id, actions))
        return True
    else:
      logger.info("[#{}] The request is unprocessable".format(id))
      return None

  def _participationAllowed(self, p):
    """Returns True if given participation is on the config else False"""
    return True if p in self.config.participations else False

  def _getActionModules(self, action_names):
    """Returns the list of actions availables"""
    return [a for a in self.config.apps if a.__name__ in action_names]
