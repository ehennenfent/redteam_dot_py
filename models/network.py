from models.hosts import Host
from data.enums import PortType

class Port(object):
    def __init__(self, num: int, t: PortType = PortType.TCP):
        self.number = num
        self.port_type = t

    def __hash__(self):
        return hash((self.number, self.port_type))

    def __eq__(self, other):
        return (self.number, self.port_type) == (other.number, other.port_type)

    def __ne__(self, other):
        return not(self == other)

    @property
    def __dict__(self):
        return {'number': self.number, 'type': self.port_type}


class NAT(object):
    router: Host = None

    def __init__(self):
        self.subnet = "192.168.*.*"
        self.set_router(Host())
        self._hosts = {}
        self._ports = {}
        self._nat = {}

    @property
    def hosts(self):
        return list(self._hosts.values()) + [self.router]

    @property
    def ports(self):
        return list(self._ports.keys()) + self.router.ports

    def set_router(self, router):
        router.set_parent(self)
        self.router = router

    def map_host(self, host, src_port=None, dest_port=None):
        host.set_parent(self)
        self._hosts[id(host)] = host
        if src_port is not None:
            self._ports[src_port] = id(host)
        if dest_port is not None:
            self._nat[src_port] = dest_port

    def get_host_by_local_ip(self, ip):
        for host in self.hosts:
            if host.local_ip == ip:
                return host

    @property
    def __dict__(self):
        return {'subnet': self.subnet,
                'router': self.router,
                '_hosts': self._hosts,
                '_ports': self._ports,
                '_nat': self._nat}
