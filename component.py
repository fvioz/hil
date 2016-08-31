# -*- coding: utf-8 -*-

from hil.decorator import HILNonOverridable, non_overridable

class HILComponent(object):

  __metaclass__ = HILNonOverridable

  @non_overridable
  def call(self, conn, id):
    results = self.run(id)
    conn.send(results)

  def run(self, id):
    raise NotImplementedError
