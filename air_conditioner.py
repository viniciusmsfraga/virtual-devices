import paho.mqtt.client as mqtt
from time import sleep
import json
import random
import argparse

objective = 33
temperature = 33

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("commands/air_conditioner")

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
	if temperature > objective:
		temperature -=1
	elif temperature < objective:
		temperature += 1
	client.publish("drivers/virtual_air", device_id+";"+str(temperature)+";")

client.loop_stop()
