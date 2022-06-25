from http import client
import paho.mqtt.client as paho
import sys
import json

import time
ts = time.time()
  
# print the current timestamp
print(ts)
print(type(ts))


cli = paho.Client()

demo = {"timestamp" : ts, "bot1" : 10, "bot2" : 10}


if cli.connect("36.255.69.54", 1883, 60) != 0:
    print("Unable to connect")
    sys.exit(-1)

cli.publish("iort", json.dumps(demo), 0)
cli.disconnect()