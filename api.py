# -*- coding: utf-8 -*-

from hug.api import API
from multiprocessing import Process
from hil.middleware import HilApiMiddleware
from wsgiref.simple_server import make_server

class HilApi:
  def __init__(self, core, module):
    self.api = API(module)
    self.api.directive('core', core)
    self.api.http.add_middleware(HilApiMiddleware(core))
    self.running = False

  def __del__(self):
    self.stop()

  def start(self, port = 8000):
    """
    Start the api server
    """
    if not self.running:
      print("Serving on port {0} ...".format(port))

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
