import hug
from falcon import HTTP_201, HTTP_400

@hug.get('/echo')
def echo(response):
  return True

@hug.post('/')
def event(request, response, component: hug.types.text, event: hug.types.text, **kwargs):
  core = request.context['core']
  trigger = core.trigger(component, event, kwargs)
  response.status = HTTP_201 if trigger else HTTP_400
  return trigger
