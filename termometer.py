from multiprocessing import Process
from time import sleep
import paho.mqtt.client as mqtt
import argparse


def termometer(device_id):
	temperature = 26.2

	def on_connect(client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		client.subscribe("devices/termometer")


	client = mqtt.Client()
	client.on_connect = on_connect

	client.connect("localhost", 1883, 60)

	client.loop_start()

	while True:
		sleep(1)
		client.publish("drivers/termometer", device_id+">"+str(temperature))

	client.loop_stop()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-s","--size", type=int,
                        help="how many device instances to create", default=1)
	args = parser.parse_args()

	for device_id in range(args.size):
		Process(target=termometer, args=(str(device_id),)).start()