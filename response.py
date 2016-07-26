import requests

class HilResponse(object):
  """docstring for ClassName"""
  def __init__(self, control, retry = 3, timeout = 3):
    self.control = control
    self.retry = retry
    self.timeout = timeout

  def call(self, url, data):
    while self.retry != 0:
      try:
        r = requests.post(url, data = data, timeout = self.timeout)
        if !(r.status in [200, 201]):
          continue
      except:
        self.cont -= 1
        continue
      break
    return self.process(r)

  def process(self, request):
    parse_request = ""
    self.control.core.logger.info(parse_request)
