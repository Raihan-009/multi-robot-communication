import paho.mqtt.client as mqtt
import time


def on_conncet (client, userdata, flags, rc):
    if rc == 0:
        print("Connected Ok!")
    else:
        print("Bad Connection : ", rc)

mqttBroker = "36.255.69.54"
client = mqtt.Client("client side script")
client.on_connect = on_conncet
print("connecting to broker :", mqttBroker)
client.connect(mqttBroker)
client.loop_start()
time.sleep(5)
client.loop_stop()
client.disconnect()