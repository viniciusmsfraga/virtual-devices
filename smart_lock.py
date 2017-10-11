import paho.mqtt.client as mqtt
from time import sleep
from multiprocessing import Process
import argparse

objective = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("commands/smart_lock")

def on_message(client, userdata, msg):
    global objective
    objective = int(msg.payload.decode())


def smart_lock(device_id):
    door_opened = 0

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.loop_start()

    while True:
        sleep(2)
        if door_opened != objective:
            door_opened = objective
        client.publish("drivers/smart_lock", device_id+";"+str(door_opened)+";")

    client.loop_stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w","--workers", type=int, help="how many worker indtsances to create", default=1)
    args = parser.parse_args()

    for worker_id in range(args.workers):
        Process(target=smart_lock, args=(str(worker_id),)).start()