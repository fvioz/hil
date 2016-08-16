# -*- coding: utf-8 -*-

import time
from hil.log import logger

class HilContext(object):
  """docstring for HilContext"""
  def __init__(self, conn, contexts):
    super(HilContext, self).__init__()
    self.conn = conn
    self.contexts = contexts
    self.data = {}
    self.runnig = False

  def __processCall(self, atype):
    if atype == 'close':
      self.runnig = False
    elif atype == 'contexts':
      self.conn.send(self.data)

  def call(self):
    self.runnig = True
    while self.runnig:
      self.run()
      if self.conn.poll():
        atype = self.conn.recv()
        self.__processCall(atype)
      time.sleep(.1)

  def run(self):
    raise NotImplementedError

  def getValue(self, key):
    if key in self.variable:
      if key in self.data:
        return self.data[key]
      else:
        return None
    else:
      return None

  def setValue(self, key, value):
    if key in self.contexts:
      self.data[key] = value
      return False
    else:
      return True
