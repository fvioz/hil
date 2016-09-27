# -*- coding: utf-8 -*-

import time
import requests

from hil.log import logger

class HILFeedback(object):
  """docstring for ClassName"""
  def __init__(self, id, callback, data, retry = 3, timeout = 10):
    self.id = id
    self.data = data
    self.retry = retry
    self.timeout = timeout
    self.callback = callback

  def run(self, child_conn):
    cont = 1
    while cont <= self.retry:
      try:
        r = requests.get(self.callback, data = { "hola": "asdasd"}, timeout = self.timeout)
        if not (r.status_code in [200, 201]):
          continue
        else:
          child_conn.send([True, r.status_code, r.text])
          break
      except Exception as e:
        last_error = str(e)
        logger.error("[#{}] Response {}º attempt to connect, Error: {}".format(self.id, cont, last_error))
        cont += 1
        continue
    else:
      child_conn.send([False, last_error])

