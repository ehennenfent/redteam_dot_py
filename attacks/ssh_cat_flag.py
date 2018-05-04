from tasks import ssh_to_host
from data.enums import Protocol

def attack(host):
    for port in host._services:
        service = host._services[port]
        if service.protocol is Protocol.SSH:
            if host.parent is not None:
                # TODO parse the tree so this works on non-flat networks without hardcoding
                ssh_to_host(host, 'cat {}'.format(host.flag_path), port=2210)
            else:
                ssh_to_host(host, 'cat {}'.format(host.flag_path), port)
