import hug
from falcon import HTTP_201, HTTP_400

@hug.get('/echo')
def echo(response):
  return True

@hug.post('/')
def event(request, response, component: hug.types.text, event: hug.types.text, *args):
  core = request.context['core']
  trigger = core.trigger(component, event, args)
  if trigger:
    response.status = HTTP_201
  else:
    response.status = HTTP_400
  return trigger

@hug.get('/test')
def test(request, response):
  core = request.context['core']
  trigger = core.trigger('Bell', 'play')
  if trigger:
    response.status = HTTP_201
  else:
    response.status = HTTP_400
  return trigger
