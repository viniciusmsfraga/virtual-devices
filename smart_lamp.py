import paho.mqtt.client as mqtt
from time import sleep
import json
import random
import argparse

temperature = 33
light = 0
objective = 0

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("devices/smart_lamp")

def on_message(client, userdata, msg):
	global objective
	objective = int(msg.payload.decode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()

parser = argparse.ArgumentParser()
parser.add_argument("id",
                    help="device id",
                    type=str)

device_id = parser.parse_args().id

while True:
	sleep(2)
	if light > objective:
		light = objective
	client.publish("drivers/smart_lamp", device_id+";"+str(light)+";")

client.loop_stop()
