from coapthon.client.helperclient import HelperClient

host = "127.0.0.1"
port = 5683
path ="independent"


# set the ``independent'' resource to "updatedValue"
client = HelperClient(server=(host, port))
response = client.put(path,"updatedValue")
client.stop()