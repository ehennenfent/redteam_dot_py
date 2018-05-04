from models.hosts import Host

class NAT(object):
    router: Host = None

    def __init__(self, ip):
        self.ip = ip
        self.subnet = "255.255.255.0"
        self.set_router(Host())
        self._hosts = {}
        self._ports = {}
        self._nat = {}

    @property
    def hosts(self):
        return list(self._hosts.values()) + [self.router]

    @property
    def ports(self):
        return list(self._ports.keys())

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

    def get_host_by_port(self, port_num):
        return self._hosts[self._ports[port_num]]

    @property
    def services(self):
        out = []
        for host in self._hosts.values():
            for service_port in host._services:
                if service_port in self._ports.keys():
                    out.append((service_port, host._services[service_port]))
                elif service_port in self._nat.values():
                    for pt in self._nat:
                        if self.nat[pt] == service_port:
                            out.append((pt, host._services[service_port]))
        return out

    @property
    def __dict__(self):
        return {'ip': self.ip,
                'subnet': self.subnet,
                'router': self.router,
                '_hosts': self._hosts,
                '_ports': self._ports,
                '_nat': self._nat}
