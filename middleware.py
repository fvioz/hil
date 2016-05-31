# -*- coding: utf-8 -*-

class HilApiMiddleware(object):
  def __init__(self, core):
    self.core = core

  def core(self):
    return self.core

  def process_request(self, request, response):
    request.context.update({ "core": self.core })

