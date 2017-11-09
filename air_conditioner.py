from multiprocessing import Process
from time import sleep
import paho.mqtt.client as mqtt
import argparse


def air_conditioner(device_id):
    objective = 33
    temperature = 33


    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("commands/air_conditioner/" + device_id)


    def on_message(client, userdata, msg):
        nonlocal objective
        objective = int(msg.payload.decode())


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_start()

    while True:
        sleep(1)
        if temperature > objective:
            temperature -=1
        elif temperature < objective:
            temperature += 1
        client.publish("drivers/virtual_air", device_id+"::"+str(temperature))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--size", type=int,
                        help="how many device instances to create", default=1)
    args = parser.parse_args()

    for device_id in range(args.size):
        Process(target=air_conditioner, args=(str(device_id),)).start()