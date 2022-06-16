from http import client
import paho.mqtt.client as paho
import sys

cli = paho.Client()


if cli.connect("36.255.69.54", 1883, 60) != 0:
    print("Unable to connect")
    sys.exit(-1)

cli.publish("test/status", "Hello from mac hehe", 0)
cli.disconnect()