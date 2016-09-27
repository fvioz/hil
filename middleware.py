# -*- coding: utf-8 -*-

class HILApiMiddleware(object):
  def __init__(self, conn):
    self.conn = conn

  def conn(self):
    return self.conn

  def process_request(self, request, response):
    request.context.update({ "conn": self.conn })

