from hosts import Host, UnknownHost
from typing import Dict, List
from data.enums import Port

class NAT(object):
    
    def __init__(self):
        
        self.router: Host = UnknownHost()
        self.tcp_map: Dict(int, Host) = {}
        self.udp_map: Dict(int, Host) = {}
        self.hidden_hosts: List(Host) = []

        
    @property
    def hosts(self):
        return self.tcp_map.values() + self.udp_map.values()
        
    @property
    def tcp_ports(self):
        return list(self.tcp_map.keys())
        
    @property
    def udp_ports(self):
        return list(self.udp_map.keys())
        
    def add_host(self, port: int, host: Host, t: Port = Port.tcp):
        if t is Port.tcp:
            self.tcp_map[port] = host
        if t is Port.udp:
            self.udp_map[port] = host
    
    # TODO: support for hidden hosts - ones that don't expose anything to NAT
    # TODO: store the subnet
    # TODO: support getting hosts by ip address
    # TODO: bind all open ports to the router host object