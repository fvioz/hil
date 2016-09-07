# -*- coding: utf-8 -*-

from hil.decorator import HILNonOverridable, non_overridable

class HILComponent(object):

  __metaclass__ = HILNonOverridable

  @non_overridable
  def call(self, conn, id, participation, role):
    results = self.run(id, participation, role)
    conn.send(results)

  def run(self, id, participation, role):
    raise NotImplementedError
