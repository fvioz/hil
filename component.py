# -*- coding: utf-8 -*-

import sys
from slugify import slugify

class HilComponent(object):

  name = __name__
  api_name = slugify(__name__)

  def __init__(self):
    super(HilComponent, self).__init__()

  @classmethod
  def __api_methods__(cls):
    object_methods = dir(object)# +
    method_list = list(set(dir(cls)) - set(dir(object_methods)))
    method_list = list(set(method_list) - set(['__api_methods__']))
    return [method for method in method_list if callable(getattr(cls, method))]
