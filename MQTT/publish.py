import paho.mqtt.client as mqtt
import time

broker_hostname = "localhost"  # Use host IP if needed, or "host.docker.internal" for Docker
port = 1883

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Connected successfully")
    else:
        print(f"Not connected, return code: {return_code}")

client = mqtt.Client()
# client.username_pw_set(username="USER", password="PWD")  # Uncomment if you have credentials
client.on_connect = on_connect

client.connect(broker_hostname, port)
client.loop_start()

topic = "test" #topic ที่ต้องการส่ง
msg_count = 0

try:
    while msg_count < 10:
        time.sleep(1)
        msg_count += 1
        massage = f"hello world {msg_count}"
        result = client.publish(topic, massage) #ใช้ส่งข้อความกับ topicที่เลือก
        status = result[0]
        if status == 0:
            print(f"{massage} to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")
            if not client.is_connected():
                print("Client disconnected unexpectedly, exiting...")
                break
finally:
    client.disconnect()
    client.loop_stop()
