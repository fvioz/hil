import hug
import time
from falcon import HTTP_202, HTTP_404, HTTP_422

@hug.get('/echo')
def echo(response):
  return True

@hug.post('/')
def event(request, response, participation: hug.types.text, callback: hug.types.text, timeout = 180):
  id = str(int(time.time()))
  control = request.context['control']
  trigger = control.trigger(id, participation, callback, int(timeout))

  if trigger == True:
    text = "Action user request accepted."
    response.status = HTTP_202
  elif trigger == False:
    text = "Action not found with current state."
    response.status = HTTP_404
  else:
    text = "Action unprocessable."
    response.status = HTTP_422

  return { "id": id, "status": response.status, "response": text }
