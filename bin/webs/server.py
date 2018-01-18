from toolkit import stat, verbo
import os
from SimpleWebSocketServer import SimpleSSLWebSocketServer, WebSocket
import thread

clients = []

class SimpleServer(WebSocket):
  def handleMessage(self):
    pass
  def handleConnected(self):
    clients.append(self)
  def handleClose(self):
    clients.remove(self)

def start_websocket_server(cert, key, port):
    stat("Starting websocket server")

    try:
      verbo("Reading SSL/TLS certificate")
      with open(cert) as f:
        pass
    except:
      stat("!! FAILED TO READ SSL/TLS CERTIFICATE !!")
      exit(2)

    try:
      verbo("Reading SSL/TLS key")
      with open(key) as f:
        pass
    except:
      stat("!! FAILED TO READ SSL/TLS PRIVATE KEY!!")
      exit(2)

    verbo("SSL/TLS Check PASSED")

    verbo("Will now start websocket server on port " + str(port))
    server = SimpleSSLWebSocketServer('', port, SimpleServer, cert, key)
    thread.start_new_thread(server.serveforever, ())
    stat("Websocket server is now running")
