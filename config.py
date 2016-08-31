# -*- coding: utf-8 -*-

import os
import json
import inspect

from hil.log import logger
from hil.context import HILContext
from hil.component import HILComponent

from jsonschema import validate

class HILConfig(object):
  """docstring for HILConfig"""
  def __init__(self, conn, apps, context, schemaFileName = "schema.json", configFileName = "hil.json"):
    super(HILConfig, self).__init__()
    self.conn = conn
    self.apps = apps
    self.context = context
    self._config = self.validateConfig(schemaFileName, configFileName)

  @property
  def participations(self):
    return list(self._config.keys())

  @property
  def contexts(self):
    data = []
    for k,v in self._config.items():
      for i in self._config[k]:
        for c in i.get("contexts"):
          data.append(c)
    return data

  @property
  def attention_levels(self):
    data = []
    for k,v in self._config.items():
      for i in self._config[k]:
        for c in list(i.get("attention_levels")):
          data.append(c)
    return data

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
        raise Exception("App must be a HILComponet class")

      if not issubclass(a, HILComponent):
        raise Exception("{0} must be a HILComponent type.".format(a.__name__))
    self._apps = apps

  @context.setter
  def context(self, c):
    if not inspect.isclass(c):
      raise Exception("Context must be a HILContext class.")

    if not issubclass(c, HILContext):
      raise Exception("{0} must be a HILContext type.".format(c.__name__))
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

  def getAction(self, participation, role):
    try:
      self.conn.send('contexts')
      data = self.conn.recv()
    except:
      data = {}

    if not participation in self._config: return None

    current_level = data.get("attention_level")
    current_participation = self._config[participation]

    for i in current_participation:

      levels = i.get("attention_levels")

      if not current_level in levels: continue

      for k, v in i.get("contexts").items():
        if data.get(k) == v:
          continue
        else:
          levels = None
          break

      if levels:
        components = []
        roles = levels.get(current_level)
        for r in role.split(':'):
          if r in roles:
            for c in roles[r]:
              components.append(c)
        if components:
          return components

    return None
