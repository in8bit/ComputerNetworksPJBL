import paho.mqtt.client as paho
import sys

broker ="192.168.1.25"
def onMessage(client, userdata, msg):
	print(msg.topic + ": "+msg.payload.decode())
	
client =paho.Client()
client.on_message =onMessage

if client.connect(broker, 1883, 60) != 0:
	print("could not connect to the broker.")
	sys.exit(-1)
	
client.subscribe("Command")
try:
    print("press ctrl+c to exit...")
    client.loop_forever()
except:
    print("Disconnecting from broker")
    
client.disconnect()