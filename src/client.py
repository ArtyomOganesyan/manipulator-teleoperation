import websocket
import json
from threading import Thread

class SensorWebSocketClient:
    def __init__(self, address, robot_controller):
        self.address = address
        self.robot_controller = robot_controller
        self.ws_a = websocket.WebSocketApp(
            f'ws://{self.address}/sensors/connect?types=["android.sensor.linear_acceleration","android.sensor.gyroscope"]',
            on_open=self.on_open,
            on_message=self.on_message_a,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws_touch = websocket.WebSocketApp(
            f'ws://{self.address}/touchscreen',
            on_open=self.on_open,
            on_message=self.on_message_touch,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def on_message_a(self, ws, message):
        data = json.loads(message)
        sensor_type = data['type']
        values = data['values']
        timestamp = data.get('timestamp', 0)
        
        # Forward data to RobotController
        self.robot_controller.update_sensor_data(sensor_type, values, timestamp)

    def on_message_touch(self, ws, message):
        data = json.loads(message)
        action = data['action']

        self.robot_controller.update_touchscreen(action)

    def on_error(self, ws, error):
        print("Error occurred:", error)

    def on_close(self, ws, close_code, reason):
        print("Connection closed:", reason)

    def on_open(self, ws):
        print("Connected to sensor server")

    def run(self):
        """Run WebSocket in a background thread."""
        self.ws_thread = Thread(target=self.ws_a.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()

        self.ws_thread_t = Thread(target=self.ws_touch.run_forever)
        self.ws_thread_t.daemon = True
        self.ws_thread_t.start()
