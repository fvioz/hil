
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
      self.components[component] = component()
    else:
      print(component.__name__, "is running.")

  def remove(self, component):
    if component in self.components:
      del self.components[component]

  def reload(self, component):
    module = sys.modules[component.__module__]
    self.components[component] = reload(module)
    return self.components[component]

  def trigger(self, component, target, args):
    print("\t Running", target, component)
    component = self.reload(component)
    if isinstance(target, str):
      target = getattr(component, target)
    event = HilEvent(component, target, args)
    event.run()
