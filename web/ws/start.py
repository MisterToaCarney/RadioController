import websocket

ws = websocket.WebSocket()

ws.connect("ws://localhost:6680/mopidy/ws")

ws.send("Test")

result = ws.recv()

print(result)

ws.close()
