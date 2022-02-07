from coapthon.client.helperclient import HelperClient

host = "127.0.0.1"
port = 5683
path ="controlled"

#Upon receiving updates, print it out
def client_callback_observe(response):
    global client
    print response

#Observe on the Controlled Value
client = HelperClient(server=(host, port))
response = client.observe(path,client_callback_observe)
