import paho.mqtt.client as mqtt
import argparse


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("drivers/#")


def on_message(client, userdata, msg):
    print(msg.payload.decode())
    client.publish("commands/air_conditioner/3", str(15))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()