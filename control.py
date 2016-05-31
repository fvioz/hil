# -*- coding: utf-8 -*-

import sys

from importlib import reload
from hil.event import HilEvent
from hil.response import HilResponse

class HilControl:
  def __init__(self, core):
    self.components = {}

  def install(self, component):
    if not (component in self.components):
      print(component.__name__, "component instaled.")
      self.components[component.__name__] = component
    else:
      print(component.__name__, "is already installed.")

  def exist(self, component_name, target = None):
    if component_name in self.components:
      if target == None:
        return True
      # FIXME
      return True
      if target in self.components[component_name]:
        return True
    return False

  def remove(self, component):
    if self.exist(component):
      del self.components[component]

  def reload(self, component):
    module = sys.modules[component.__module__]
    self.components[component] = reload(module)
    return self.components[component]

  def trigger(self, component_name, target, args):
    if self.exist(component_name, target):
      print("\t Running", target, component_name)
      component = self.reload(self.components[component_name])
      if isinstance(target, str):
        target = getattr(klass, target)
      event = HilEvent(component, target, args)
      event.run()
      return True
    else:
      return False

  def stop(self):
    return
