# -*- coding: utf-8 -*-

class HilApiMiddleware(object):
  def __init__(self, control):
    self.control = control

  def control(self):
    return self.control

  def process_request(self, request, response):
    request.context.update({ "control": self.control })

