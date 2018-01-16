from toolkit import stat
import websocket as websocketclient
import time
import globals

def start_websocket_client(host, port):
    def websocket_open(ws):
        stat("Connected to WebSocket server.")
        global connected
        if (connected == False):
            connected = True

    def websocket_message(ws, message):
        if(globals.args.verbose):
            stat(str(message))


    def websocket_error(ws, error):
        if ("Errno 111" in str(error)):
            pass
        else:
            stat(str(ws) + " " + str(error))

    def websocket_close(ws):
        stat("WebSocket Closed")
    stat("Starting client")
    url = "ws://"+str(host)+":"+str(port)+"/mopidy/ws"
    stat("URL is " + url)

    ws = websocketclient.WebSocketApp(url, on_message = websocket_message, on_error = websocket_error, on_close = websocket_close, on_open = websocket_open)

    global connected
    connected = False
    stat("Waiting for music server to accept connection...")

    while (connected == False):
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            ws.close()
            return(0)
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            return(0)
