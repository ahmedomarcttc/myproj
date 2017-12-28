import logging
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)

class demotopo(DCNetwork):
    """
    This is a 4 PoP round topology used for the emulator MANO integration demo.
    """

    def __init__(self):
        """
        Initialize multi PoP emulator network.
        """
        super(demotopo, self).__init__(
            monitor=True,
            enable_learning=True
        )
	# define members for later use
        nofnodes = 4
        for s in range(nofnodes):
            exec 'self.pop%s = None'%(s+1)
        for s in range(nofnodes):
            exec 'self.sw%s = None'%(s+1)

    def setup(self):
        self._create_switches()
        self._create_pops()
        self._create_links()
        self._create_rest_api_endpoints()
        self._create_openstack_api_endpoints()
#        self._create_dummygk_api_endpoints()

    def _create_switches(self):
        for s in range(4):
            exec 'self.sw%s = self.addSwitch("sw%s")'%(s+1, s+1)

    def _create_pops(self):
        # two PoPs for the OSM SP
        for s in range(4):
            exec 'self.pop%s = self.addDatacenter("osm-pop%s")'%(s+1, s+1)

    def _create_links(self):
        # OSM island
        self.addLink(self.pop1, self.sw1)
        self.addLink(self.pop2, self.sw2)
        self.addLink(self.pop3, self.sw3)
        self.addLink(self.pop4, self.sw4)
        self.addLink(self.sw1, self.sw2)
        self.addLink(self.sw2, self.sw3)
        self.addLink(self.sw3, self.sw4)
        self.addLink(self.sw4, self.sw1)

    def _create_openstack_api_endpoints(self):
        # create
        api1 = OpenstackApiEndpoint("172.31.255.1", 6001)
        api2 = OpenstackApiEndpoint("172.31.255.1", 6002)
        api3 = OpenstackApiEndpoint("172.31.255.1", 6003)
        api4 = OpenstackApiEndpoint("172.31.255.1", 6004)
        # connect PoPs
        api1.connect_datacenter(self.pop1)
        api2.connect_datacenter(self.pop2)
        api3.connect_datacenter(self.pop3)
        api4.connect_datacenter(self.pop4)
        # connect network
        api1.connect_dc_network(self)
        api2.connect_dc_network(self)
        api3.connect_dc_network(self)
        api4.connect_dc_network(self)
        # start
        api1.start()
        api2.start()
        api3.start()
        api4.start()

    def _create_rest_api_endpoints(self):
        # create
        apiR = RestApiEndpoint("0.0.0.0", 5001)
        # connect PoPs
        apiR.connectDatacenter(self.pop1)
        apiR.connectDatacenter(self.pop2)
        apiR.connectDatacenter(self.pop3)
        apiR.connectDatacenter(self.pop4)
        # connect network
        apiR.connectDCNetwork(self)
        # start
        apiR.start()

    # def _create_dummygk_api_endpoints(self):
    #     # create
    #     apiSDK = SonataDummyGatekeeperEndpoint("0.0.0.0", 5000)
    #     # connect PoPs
    #     apiSDK.connectDatacenter(self.pop1)
    #     apiSDK.connectDatacenter(self.pop2)
    #     # start
    #     apiSDK.start()


def main():
    t = demotopo()
    t.setup()
    t.start()
    t.CLI()
    t.stop()


if __name__ == '__main__':
    main()
