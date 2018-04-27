from models.network import NAT, Port
from models.hosts import LinuxHost, WindowsHost, Service
from data.enums import PortType, Protocol

defaultpw = "Hack the planet!"

network = NAT()

router = LinuxHost("Gateway", flag_path="/etc/flag.txt")
router.map_service(Port(53, t=PortType.UDP), Service("DNS", Protocol.DNS))
router.map_service(Port(80), Service("HTTP", Protocol.HTTP))
router.map_service(Port(2201), Service("SSH", Protocol.SSH, default_credentials=('cs460', defaultpw)))
network.set_router(router)

linux = LinuxHost("Linux Server", flag_path="/cs460/flag.txt")
linux.map_service(Port(22), Service("SSH", Protocol.SSH, default_credentials=('cs460', defaultpw)))
linux.map_service(Port(21), Service("FTP (Command)", Protocol.FTP, default_credentials=('cs460', defaultpw)))
linux.map_service(Port(20), Service("FTP (Data)", Protocol.FTP, default_credentials=('cs460', defaultpw)))
linux.map_service(Port(5222), Service("Jabber", Protocol.XMPP, default_credentials=('cs460', defaultpw)))
linux.map_service(Port(80), Service("WordPress/Joomla?", Protocol.HTTP, default_credentials=('cs460', defaultpw)))
linux.map_service(Port(3306), Service("MySQL", Protocol.SQL, default_credentials=('root', 'root')))
network.map_host(linux, Port(2210), Port(22))
network.map_host(linux, Port(2110), Port(21))
network.map_host(linux, Port(2010), Port(20))
network.map_host(linux, Port(5222))
network.map_host(linux, Port(80))
network.map_host(linux, Port(3306))


winserv = WindowsHost("Windows Server", flag_path="C:\\Shares\\DomainFolder\\flag.txt")
winserv.map_service(Port(5903), Service("Remote Desktop (TCP)", Protocol.RDP, default_credentials=('Administrator', defaultpw)))
winserv.map_service(Port(5903, t=PortType.UDP), Service("Remote Desktop (UDP)", Protocol.RDP, default_credentials=('Administrator', defaultpw)))
for service_port in winserv._services.keys():
    network.map_host(winserv, service_port)

windesk = WindowsHost("Windows Desktop", flag_path="C:\\flag.txt")
windesk.map_service(Port(5904), Service("Remote Desktop (TCP)", Protocol.RDP, default_credentials=('AD\\cs460', defaultpw)))
windesk.map_service(Port(5904, t=PortType.UDP), Service("Remote Desktop (UDP)", Protocol.RDP, default_credentials=('AD\\cs460', defaultpw)))
for service_port in windesk._services.keys():
    network.map_host(windesk, service_port)

kali = LinuxHost("Kali Desktop")
network.map_host(kali)

def encode_complex(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__

import simplejson as json
with open('out.json', 'w') as outfile:
    encoded = json.dumps(network, default=encode_complex)
    outfile.write(encoded)

# import dill as pickle
# with open('460.bin', 'wb') as outfile:
#     pickle.dump(network, outfile)
#
# with open('460.bin', 'rb') as infile:
#     n = pickle.load(infile)
