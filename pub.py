from http import client
import paho.mqtt.client as paho
import sys
import json

cli = paho.Client()

demo = {"bot1" : 10, "bot2" : 15}


if cli.connect("36.255.69.54", 1883, 60) != 0:
    print("Unable to connect")
    sys.exit(-1)

cli.publish("iort", json.dumps(demo), 0)
cli.disconnect()