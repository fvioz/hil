# -*- coding: utf-8 -*-

import threading
import multiprocessing

from hil.log import logger
from hil.box import HilBox
from hil.config import HilConfig

class HilControl:
  def __init__(self, config):
    self.config = config
    self.parent_conn, self.child_conn = multiprocessing.Pipe()
    self.current_context = self.config.context(self.child_conn, self.config.contexts)
    multiprocessing.Process(target=self.current_context.call).start()

  def __del__(self):
    self.parent_conn.send('close')

  def trigger(self, id, participation, callback, timeout):
    """Launchs the current process .

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    if self.__participationAllowed(participation) == True:
      action_name = self.config.getAction(self.parent_conn, participation)
      if action_name == None:
        logger.info("[#{}] The request did not have any action".format(id))
        return False
      else:
        actions = self.__getActionModules(action_name)
        box = HilBox(id, actions, callback, timeout)
        t = threading.Thread(target=box.run, args=())
        t.setDaemon(True)
        t.start()
        logger.info("[#{}] Actions {} launched".format(id, actions))
        return True
    else:
      logger.info("[#{}] The request is unprocessable".format(id))
      return None

  def __participationAllowed(self, p):
    """Returns True if given participation is on the config else False"""
    return True if p in self.config.participations else False

  def __getActionModules(self, action_names):
    """Returns the list of actions availables"""
    return [a for a in self.config.apps if a.__name__ in action_names]
