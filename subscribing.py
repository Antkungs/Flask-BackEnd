from datetime import datetime
import json
import paho.mqtt.client as mqtt
import time
import psycopg2
from psycopg2 import sql
import app
DATABASE = {
    'dbname': 'topguntest',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}
def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Connected successfully")
        client.subscribe("prediction/gender") #topic ที่ต้องการรับ
    else:
        print(f"Not connected, return code: {return_code}")
        client.failed_connect = True

def on_message(client, userdata, message):
    try:
        # Decode the payload and parse as JSON
        payload = str(message.payload.decode("utf-8"))
        print("Received message: ", payload)

        msg_data = json.loads(payload)
        print(msg_data)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        predicted_gender = msg_data.get("predicted_gender", "")
        confidence_score = msg_data.get("confidence_score", "")
        app.insert_voice_analysis(current_time,predicted_gender,confidence_score)
        
    except Exception as e:
        print(f"Error parsing message: {e}")


broker_hostname = "localhost"  # Use host IP if needed, or "host.docker.internal" for Docker
port = 1883

client = mqtt.Client()
# client.username_pw_set(username="USER", password="PWD")  # Uncomment if you have credentials
client.on_connect = on_connect 
client.on_message = on_message 
client.failed_connect = False

client.connect(broker_hostname, port)
client.loop_start()

try:
    i = 0
    while True and not client.failed_connect:
        time.sleep(1)
        i += 1
    if client.failed_connect:
        print("Connection failed, exiting...")

finally:
    client.disconnect()
    client.loop_stop()
