import paho.mqtt.client as mqtt
import socket
import time
host = socket.gethostname()

def on_connect(client, userdata, flags, rc):
    print("Connected - rc:", rc)
def on_message(client, userdata, message):
    global FLAG
    global chat
    if str(message.topic) != pubtop:
        msg = str(message.payload.decode("utf-8"))
        print(str(message.topic), msg)
        if msg == "Stop" or msg == "stop":
            FLAG = False
        else:
            chat = input("Enter Message: ")
            client.publish(pubtop, chat)
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))
def on_unsubscirbe(client,userdata,mid):
    print("Unsubscribed:", str(mid))
def on_disconnect(client,userdata,rc):
    if rc !=0:
        print("Unexpected Disconnection")


broker_address = host
port = 1883

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscirbe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)

time.sleep(1)

pubtop = "/chat/client2"
subtop = "/chat/client1"
FLAG = True
chat = None

client.loop_start()
client.subscribe(subtop)
while True:
    if FLAG is False or chat == "Stop" or chat == "stop":
        break

client.disconnect()
client.loop_stop()
