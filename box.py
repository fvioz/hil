# -*- coding: utf-8 -*-

import time
import multiprocessing

from hil.log import logger
from hil.feedback import HILFeedback

class HILBox(object):
  """docstring for HILBox"""
  def __init__(self, id, participation, role, actions, callback, timeout):
    super(HILBox, self).__init__()
    self.id = id
    self.role = role
    self.participation = participation
    self.actions = actions
    self.callback = callback
    self.timeout = timeout
    self.processes = []
    self.start = time.time()
    self.context = multiprocessing.get_context('spawn')
    self.parent_conn, self.child_conn = multiprocessing.Pipe()

  def launchProcess(self):
    for action in self.actions:
      p = self.context.Process(target=action().call, args=(self.child_conn, self.id, self.participation, self.role))
      p.start()
      self.processes.append(p)
      logger.info("[#{}] Process {} started".format(self.id, action))

  def processResponse(self):
    responses = [self.parent_conn.recv() for p in self.processes]
    logger.info("[#{}] Proces output {}".format(self.id, responses))

    current_timeout = (time.time() - self.start)
    req = HILFeedback(self.id, self.callback, responses, timeout = 2)
    p = self.context.Process(target=req.run, args=(self.child_conn,))
    p.start()

    res = self.parent_conn.recv()
    remain = time.time() - self.start

    if res[0] == True:
      logger.info("[#{}] Process ended in {} seconds with status {} and body {}".format(self.id, str(remain), res[1], res[2]))
    else:
      logger.info("[#{}] Process ended in {} seconds with error {}".format(self.id, str(remain), res[1]))

  def timeoutProcess(self):
    for p in self.processes:
      if p.is_alive():
        p.terminate()
      p.join()
    logger.info("[#{}] Process timeout".format(self.id))

  def run(self):
    self.launchProcess()
    while time.time() - self.start <= self.timeout:
      if all(not p.is_alive() for p in self.processes):
        self.processResponse()
        break
      else:
        time.sleep(.1)  # Just to avoid hogging the CPU
    else:
      self.timeoutProcess()
