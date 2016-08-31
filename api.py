# -*- coding: utf-8 -*-

from hug.api import API
from multiprocessing import Process
from hil.middleware import HILApiMiddleware
from wsgiref.simple_server import make_server

class HILApi:
  def __init__(self, module, conn):
    self.api = API(module)
    self.conn = conn
    self.running = False

  def __del__(self):
    self.stop()

  def start(self, port = 8000):
    """
    Start the api server
    """
    self.api.directive('conn', self.conn)
    self.api.http.add_middleware(HILApiMiddleware(self.conn))

    if not self.running:
      print("=> Application starting on 0.0.0.0:{0}".format(port))
      print("=> Ctrl-C to shutdown server\n")

      sv = self.api.http.server()
      httpd = make_server('', port, sv)

      self.__server_process = Process(target=httpd.serve_forever)
      self.__server_process.start()
      self.running = True

  def stop(self):
    """
    Stop the api server
    """
    if self.running:
      self.__server_process.terminate()
      self.__server_process.join()
      self.running = False
