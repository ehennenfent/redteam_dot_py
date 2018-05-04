from models.network import NAT
from models.hosts import LinuxHost, WindowsHost, Service
from data.enums import Protocol
from attacks import ssh_cat_flag

defaultpw = "Hack the planet!"
networks = []
for i in range(2,28):
    if i == 24:
        continue

    network = NAT("192.168.101.{}".format(i))

    router = LinuxHost("Gateway", local_ip="192.168.{}.1".format(i), flag_path="/etc/flag.txt")
    router.map_service(-53, Service("DNS", Protocol.DNS))
    router.map_service(80, Service("HTTP", Protocol.HTTP))
    router.map_service(2201, Service("SSH", Protocol.SSH, default_credentials=('cs460', defaultpw)))
    network.set_router(router)

    linux = LinuxHost("Linux Server", local_ip="192.168.{}.10".format(i), flag_path="/cs460/flag.txt")
    linux.map_service(22, Service("SSH", Protocol.SSH, default_credentials=('cs460', defaultpw)))
    linux.map_service(21, Service("FTP (Command)", Protocol.FTP, default_credentials=('cs460', defaultpw)))
    linux.map_service(20, Service("FTP (Data)", Protocol.FTP, default_credentials=('cs460', defaultpw)))
    linux.map_service(5222, Service("Jabber", Protocol.XMPP, default_credentials=('cs460', defaultpw)))
    linux.map_service(80, Service("WordPress/Joomla?", Protocol.HTTP, default_credentials=('cs460', defaultpw)))
    linux.map_service(3306, Service("MySQL", Protocol.SQL, default_credentials=('root', 'root')))
    linux.add_attack(ssh_cat_flag.attack)
    network.map_host(linux, 2210, 22)
    network.map_host(linux, 2110, 21)
    network.map_host(linux, 2010, 20)
    network.map_host(linux, 5222)
    network.map_host(linux, 80)


    winserv = WindowsHost("Windows Server", local_ip="192.168.{}.20".format(i), flag_path="C:\\Shares\\DomainFolder\\flag.txt")
    winserv.map_service(5903, Service("Remote Desktop (TCP)", Protocol.RDP, default_credentials=('Administrator', defaultpw)))
    winserv.map_service(-5903, Service("Remote Desktop (UDP)", Protocol.RDP, default_credentials=('Administrator', defaultpw)))
    for service_port in winserv._services.keys():
        network.map_host(winserv, service_port)

    windesk = WindowsHost("Windows Desktop", local_ip="192.168.{}.30".format(i), flag_path="C:\\flag.txt")
    windesk.map_service(5904, Service("Remote Desktop (TCP)", Protocol.RDP, default_credentials=('AD\\cs460', defaultpw)))
    windesk.map_service(-5904, Service("Remote Desktop (UDP)", Protocol.RDP, default_credentials=('AD\\cs460', defaultpw)))
    for service_port in windesk._services.keys():
        network.map_host(windesk, service_port)

    kali = LinuxHost("Kali Desktop", local_ip="192.168.{}.2".format(i))
    network.map_host(kali)

    networks.append(network)

import jsonpickle as json
with open('out.json', 'w') as outfile:
    encoded = json.encode(networks)
    outfile.write(encoded)
    decoded = json.decode(encoded)
