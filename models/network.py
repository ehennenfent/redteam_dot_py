from hosts import Host, UnknownHost
from typing import Dict, List
from data.enums import Port

class NAT(object):

    def __init__(self):

        self.router: Host = UnknownHost()
        self.tcp_map: Dict(int, Host) = {}
        self.hidden_hosts: List(Host) = []


    @property
    def hosts(self):
        return self.tcp_map.values()

    @property
    def tcp_ports(self):
        return list(self.tcp_map.keys())

    def add_host(self, port: int, host: Host):
        self.tcp_map[port] = host

    # TODO support udp
    # TODO: support for hidden hosts - ones that don't expose anything to NAT
    # TODO: store the subnet
    # TODO: support getting hosts by ip address
    # TODO: bind all open ports to the router host object
