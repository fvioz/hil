# -*- coding: utf-8 -*-

def non_overridable(f):
  f.non_overridable = True
  return f

def get_non_overridables(bases):
  ret = []
  for source in bases:
    for name, attr in source.__dict__.items():
      if getattr(attr, "non_overridable", False):
        ret.append(name)
    ret.extend(get_non_overridables(source.__bases__))
  return ret

class HILNonOverridable(type):
  def __new__(cls, name, bases, dct):
    non_overridables = get_non_overridables(bases)
    for name in dct:
        if name in non_overridables:
            raise Exception("You can not override {}, it is non-overridable".format(name))
    return type.__new__(cls, name, bases, dct)

