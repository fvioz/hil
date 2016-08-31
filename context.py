# -*- coding: utf-8 -*-

import time

from hil.log import logger
from hil.decorator import HILNonOverridable, non_overridable

class HILContext(object):

  __metaclass__ = HILNonOverridable

  def __init__(self, conn, contexts):
    object.__setattr__(self, "_conn", conn)
    object.__setattr__(self, "running", False)
    contexts.append("attention_level")
    for c in contexts:
      object.__setattr__(self, c, None)

  def __getattr__(self, name):
    try:
      return self.__dict__[name]
    except KeyError:
      msg = "'{0}' object has no attribute '{1}'"
      raise AttributeError(msg.format(type(self).__name__, name))

  def __setattr__(self, name, value):
    if (name in self.__dict__) and (not name in self._protectedAttributes()):
      super(HILContext, self).__setattr__(name, value)
    else:
      msg = "'{0}' object has no attribute '{1}'"
      raise AttributeError(msg.format(type(self).__name__, name))

  @non_overridable
  def call(self):
    object.__setattr__(self, "running", True)
    while self.running:
      self.run()
      if self._conn.poll():
        atype = self._conn.recv()
        self._processCall(atype)
      time.sleep(.1)

  @non_overridable
  def _processCall(self, atype):
    if atype == 'close':
      object.__setattr__(self, "running", False)
    elif atype == 'contexts':
      self._conn.send(self._currentData())

  @non_overridable
  def _currentData(self):
    return { k: v for k, v in self.__dict__.items() if not k in self._protectedAttributes() }

  @non_overridable
  def _protectedAttributes(self):
    return ['_conn', 'running']

  def run(self):
    raise NotImplementedError
