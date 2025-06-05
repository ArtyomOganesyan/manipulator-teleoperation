import websocket
import json


def on_message(ws, message):
    values = json.loads(message)['values']
    type = json.loads(message)['type']
    print("type = ", type)
    print("values = ",values)

def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    print("connection closed : ", reason)
    
def on_open(ws):
    print("connected")
    

def connect(url):
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
 

connect('ws://172.29.42.32:8080/sensors/connect?types=["android.sensor.accelerometer","android.sensor.gyroscope"]') 