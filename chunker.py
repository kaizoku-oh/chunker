import argparse
from functools import partial
import paho.mqtt.client as mqtt

binary_file = {}
chunk_size = {}
server = {}
port = {}
topic = {}

data = {
  "chunk length": 5,
  "chunk_address": 0x123,
  "chunk_content": [
    0x123,
    0x456,
    0x789,
    0xABC,
    0xDEF
  ]
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connected with result code: " + str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  # client.subscribe("$SYS/#")
  with open(binary_file, 'rb') as file:
    for chunk in iter(partial(file.read, chunk_size), b''):
      send_data(client, chunk)
  client.disconnect()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  print("Received message: " + msg.topic + " " + str(msg.payload))

def send_data(client, chunk):
  print(chunk)
  client.publish(topic, chunk)

def main():
  global binary_file
  global chunk_size
  global server
  global port
  global topic

  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()

  ap.add_argument("-f", "--file", type=str, default="firmware.bin", help="binary file path")
  ap.add_argument("-c", "--chunk", type=int, default=256, help="chunk size")
  ap.add_argument("-s", "--server", type=str, default="test.mosquitto.org", help="broker address")
  ap.add_argument("-p", "--port", type=int, default=1883, help="broker port")
  ap.add_argument("-t", "--topic", type=str, default="ota/chunker", help="mqtt topic")

  args, unknown = ap.parse_known_args()
  args = vars(args)

  binary_file = args['file']
  chunk_size = args['chunk']
  server = args['server']
  port = args['port']
  topic = args['topic']

  print("file name: {}".format(binary_file))
  print("chunk size: {}".format(chunk_size))

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  client.connect(server, port, 60)

  # Blocking call that processes network traffic, dispatches callbacks and
  # handles reconnecting.
  # Other loop*() functions are available that give a threaded interface and a
  # manual interface.
  client.loop_forever()

if __name__ == "__main__":
  main()