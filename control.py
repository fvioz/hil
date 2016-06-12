# -*- coding: utf-8 -*-

import sys
import inspect
import importlib
import multiprocessing

from hil.response import HilResponse
from hil.component import HilComponent

class HilControl:
  def __init__(self, core):
    self.klasses = []

  def exist(self, klass, target = None):
    if klass in self.klasses:
      if target == None:
        return True
      else:
        if target in klass.__dict__:
          return True
        else:
          return False
    else:
      return False

  def get_klass(self, klass_name):
    for klass in self.klasses:
      if klass.__name__ == klass_name:
        return klass
    return False

  def install(self, klass):
    if not inspect.isclass(klass):
      raise TypeError("Component should be a HilComponet Class")

    if not issubclass(klass, HilComponent):
      raise TypeError("Param must be of type HilComponent")

    if not (klass in self.klasses):
      print(klass.__name__, "component instaled.")
      self.klasses.append(klass)
    else:
      print(klass.__name__, "is already installed.")

  def remove(self, klass):
    if self.exist(klass):
      del self.klasses[klass]
      return True
    else:
      return False

  def reload(self, klass):
    module = importlib.reload(klass.__module__)
    return self.klasses[klass]

  def trigger(self, klass_name, target, args):
    klass = self.get_klass(klass_name)
    if not klass:
      return False

    if self.exist(klass, target):
      print("\t Running", target, klass_name)
      # component = self.reload(self.klasses[klass_name])
      if isinstance(target, str):
        target = getattr(klass, target)
      self.run(target, args)
      return True
    else:
      return False

  def run(self, target, args):
    context = multiprocessing.get_context('spawn')
    pr = context.Process(target=target, args=args)
    pr.start()
    # TODO: join the proccess Thread < pr.join() >
    pass

  def stop(self):
    return
