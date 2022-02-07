import getopt
import sys
import time
from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP

#IndependentResource: the value changes upon receiving an udpate fromt a client
# initial value: IRInitvalue
class IndependentResource(Resource):
    def __init__(self, name="IndependentResource", ControlledResource = None, coap_server=None):
        super(IndependentResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "IRInitValue"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        self.controlledResource = ControlledResource

    def render_GET(self, request):
        return self

    # when receiving any update, check if the controlled Resource needs to be updated as well.
    # after updating the ControlledResource, notify the coAP Server, so that the server will update all observing clients
    def render_PUT(self, request):
        self.edit_resource(request)
        if self.controlledResource.payload != request.payload:
            self.controlledResource.payload = request.payload
            self._coap_server.notify(self.controlledResource)
        return self


class ControlledResource(Resource):
    def __init__(self, name="ControlledResource", coap_server=None):
        super(ControlledResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "CRInitValue"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.edit_resource(request)
        return self


class testServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        controlledResource = ControlledResource()
        # pass both the coAP Server and the controlled resource to the independentResource, so that it can modify the value of the controlledResource, and notify the server.
        independentResource = IndependentResource(ControlledResource= controlledResource, coap_server=self)
        self.add_resource('controlled/', controlledResource)
        self.add_resource('independent/', independentResource)

        print "CoAP Server start on " + host + ":" + str(port)
        print self.root.dump()


if __name__ == "__main__":  # pragma: no cover
    ip = "0.0.0.0"
    port = 5683
    multicast = False

    server = testServer(ip, port, multicast)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."
