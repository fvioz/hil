from flask.ext.api import FlaskAPI
from multiprocessing import Process

class HilApi:
  def __init__(self, core):
    self.app = FlaskAPI(__name__)
    self.core = core
    self.server = Process(target=self.run, args=())
    self.setRoutes()
    self.start()

  def events(event):
    """
    Retrieve avalaible events.
    """
    return {}

  def createEvent(event):
    """
    Create an event.
    """
    param = str(request.data.get('text', ''))
    return '', status.HTTP_201_CREATED

  def run(self):
    self.app.run(host='127.0.0.1', port=5000, debug=True)

  def setRoutes(self):
    """ Set all routes """
    # Events
    self.app.add_url_rule('/events', 'events', self.events, methods=['GET'])
    self.app.add_url_rule('/events/<string:event>', 'events/<string:event>', self.createEvent, methods=['POST'])

  def start(self):
    self.server.start()

  def stop():
    server.terminate()
    server.join()

