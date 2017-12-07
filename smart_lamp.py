from multiprocessing import Process
from time import sleep
import paho.mqtt.client as mqtt
import argparse


def smart_lamp(device_id):
	light = 0
	objective = 0

	def on_connect(client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		client.subscribe("devices/smart_lamp/" + device_id)

	def on_message(client, userdata, msg):
		nonlocal objective
		objective = int(msg.payload.decode())


	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect("localhost", 1883, 60)

	client.loop_start()

	while True:
		sleep(2)
		if light != objective:
			light = objective
		client.publish("drivers/smart_lamp", device_id+"="+str(light)+"=")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-s","--size", type=int,
                        help="how many device instances to create", default=1)
	args = parser.parse_args()

	for device_id in range(args.size):
		Process(target=smart_lamp, args=(str(device_id),)).start()