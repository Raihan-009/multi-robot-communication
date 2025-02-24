from email import message
from pydoc import cli
import paho.mqtt.client as mqtt
import json
import os
import time

client=mqtt.Client()
IP = "36.255.69.54"
PORT = 1883
client.connect(IP, PORT, 60)

latency = []

def on_connect(client,userdata,flags,rc):
     print('Connected with result code:'+str(rc))
     client.subscribe('iort')

def on_message(_, userdata, msg):
    data = msg.payload.decode('utf-8')
    print("***************")
    print(json.loads(data), '\nTime in system:', time.time(), '\nLatency:',float(time.time()) - float(json.loads(data).get('timestamp')))
    bot1 = json.loads(data).get("bot1")
    bot2 = json.loads(data).get("bot2")

    if bot1<=bot2:
        print("Task allocated to bot1")
        client.publish("bot1", "f")
    else:
        print("Task allocated to bot2")
        client.publish("bot2", "f")
    # latency.append(float(time.time()) - float(json.loads(data).get('timestamp')))
    # print(latency)
    print("***************\n")

client.on_connect=on_connect
client.on_message=on_message
client.loop_forever()