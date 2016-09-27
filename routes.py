import hug
import time
from falcon import HTTP_202, HTTP_404, HTTP_422

@hug.get('/echo')
def echo(response):
  return True

@hug.post('/')
def event(request, response, participation: hug.types.text, role: hug.types.text, callback: hug.types.text, timeout = 180):
  id = str(int(time.time()))
  conn = request.context['conn']

  try:
    conn.send({
      "id": id,
      "participation": participation,
      "role": role,
      "callback": callback,
      "timeout": int(timeout)
    })
    res = conn.recv()
  except:
    res = None

  if res == True:
    text = "Action user request accepted."
    response.status = HTTP_202
  elif res == False:
    text = "Action not found with current state."
    response.status = HTTP_404
  else:
    text = "Action unprocessable."
    response.status = HTTP_422

  return { "id": id, "status": response.status, "response": text }
