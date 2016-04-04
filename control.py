# -*- coding: utf-8 -*-
from importlib import reload

class HilControl:
  def __init__(self, core):
    self.events = {}
    self.components = {}

  def __del__(self):
    pass

  def install(self, component):
    if True: #!self.components.has_key(component):
      instance = self.components[component] = component()
      try:
        for event, fn in instance.events:
          self.subscribe(component, event, fn)
      except:
        pass
    else:
      print("This component is running.")

  def reload(self, component):
    self.components[component.__name__] = reload(component)

  def remove(self, component):
    if self.events.has_key(component):
      del self.events[component]
    if self.components.has_key(component):
      del self.components[component]

  def subscribe(self, component, event, fn):
    if not self.events.has_key(component):
      self.events[component] = {}
    self.events[component][event] = fn

  def unsubscribe(self, component, event, fn):
    if self.events.has_key(component) and self.events[component].has_key(event):
      del self.events[component][event]
    else:
      return False


  def trigger(self, component, event, data):
    if self.events.has_key(component) and self.events[component].has_key(event):
      fn = self.events[component][event]
      return fn(data)
    else:
      return False



