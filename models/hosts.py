import weakref
from typing import Dict, List
from data.enums import OS

class Host(object):
    parent = None
    _services = {}
    os = OS.Other

    def __init__(self, name="", local_ip="", flag_path=None):
        self.name = name
        self.local_ip = local_ip
        self.flag_path = flag_path

    def set_parent(self, parent):
        self.parent = weakref.ref(parent)

    def map_service(self, port, service):
        self._services[port] = service
        service.set_parent(self)

    @property
    def __dict__(self):
        return {'name': self.name,
                'os': self.os,
                'local_ip': self.local_ip,
                'flag_path': self.flag_path,
                '_services': self._services}

class WindowsHost(Host):
    os = OS.Windows

class LinuxHost(Host):
    os = OS.Linux

class Service(object):
    parent = None

    def __init__(self, name, protocol, default_credentials=None):
        self.name = name
        self.protocol = protocol
        self.credentials = [] if default_credentials is None else [default_credentials]

    def set_parent(self, parent):
        self.parent = weakref.ref(parent)

    @property
    def __dict__(self):
        return {'name': self.name,
                'local_ip': self.local_ip,
                'protocol': self.protocol,
                'credentials': self.credentials}
