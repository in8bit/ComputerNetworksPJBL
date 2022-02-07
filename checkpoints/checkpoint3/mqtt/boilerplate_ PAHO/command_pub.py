import paho.mqtt.client as paho
import sys

broker = "192.168.1.25"
client = paho.Client()

if client.connect(broker,1883,60) !=0:
	print("could not connect to the borker")
	sys.exit(-1)
	
client.publish("Command", "lock",0)

client.disconnect()
