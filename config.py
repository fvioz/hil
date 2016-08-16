# -*- coding: utf-8 -*-

import os
import json
import inspect

from hil.log import logger
from hil.context import HilContext
from hil.component import HilComponent

from jsonschema import validate

class HilConfig(object):
  """docstring for HilConfig"""
  def __init__(self, apps, context, schemaFileName = "schema.json", configFileName = "hil.json"):
    super(HilConfig, self).__init__()

    config = self.validateConfig(schemaFileName, configFileName)

    self.participations = config.get("participations")
    self.contexts       = config.get("contexts")
    self.actions        = config.get("actions")
    self.transitions    = config.get("transitions")
    self.apps           = apps
    self.context        = context

  @property
  def participations(self):
    return self._participations

  @participations.setter
  def participations(self, p):
    self._participations = p

  @property
  def contexts(self):
    return self._contexts

  @contexts.setter
  def contexts(self, c):
    self._contexts = c

  @contexts.deleter
  def contexts(self):
    del self._contexts

  @property
  def actions(self):
    return self._actions

  @actions.setter
  def actions(self, a):
    self._actions = a

  @property
  def transitions(self):
    return self._transitions

  @transitions.setter
  def transitions(self, p):
    self._transitions = p

  @property
  def apps(self):
    return self._apps

  @apps.setter
  def apps(self, a):
    self._apps = a

  @property
  def context(self):
    return self._context

  @context.setter
  def context(self, c):
    self._context = c

  @apps.setter
  def apps(self, apps):
    apps = list(set(apps))
    for a in apps:
      if not inspect.isclass(a):
        raise Exception("App must be a HilComponet class")

      if not issubclass(a, HilComponent):
        raise Exception("{0} must be a HilComponent type.".format(a.__name__))
    self._apps = apps

  @context.setter
  def context(self, c):
    if not inspect.isclass(c):
      raise Exception("Context must be a HilContext class.")

    if not issubclass(c, HilContext):
      raise Exception("{0} must be a HilContext type.".format(c.__name__))
    self._context = c

  def validateConfig(self, schemaFileName, configFileName):
    content = ''
    try:
      with open(os.path.join(os.path.dirname(__file__), schemaFileName), 'r') as file:
        content = json.loads(file.read())
    except:
      raise Exception("Error reading schema file")

    schema = content

    content = ''

    try:
      with open(os.path.join(os.getcwd(), configFileName), 'r') as file:
        content = json.loads(file.read())
    except:
      raise Exception("Error reading hil.json config file")
    config = content

    try:
      validate(config, schema)
    except:
      raise Exception("Configuration hil.json invalid")

    return config

  def getAction(self, conn, participation):
    result = None

    try:
      conn.send('contexts')
      data = conn.recv()
    except:
      data = {}

    for i in self.transitions[participation]:
      result = i['result']
      for j in self.contexts:
        if i[j] == '*' or ((j in data) and (i[j] == data[j])):
          continue
        else:
          result = None
          break
    return result


