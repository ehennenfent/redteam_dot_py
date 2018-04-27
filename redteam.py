from collections import OrderedDict
from tasks import MonitorTask, ssh_to_host
from data.enums import Protocol
import concurrent.futures

header = """
_________________________________________
           _ _
 ___ ___ _| | |_ ___ ___ _____   ___ _ _
|  _| -_| . |  _| -_| .'|     |_| . | | |
|_| |___|___|_| |___|__,|_|_|_|_|  _|_  |
                                |_| |___|
_________________________________________
"""

targets = []
tasks = []
futures = []
scan = None

def import_ad():
    global target
    from build_460_models import networks
    target = networks

def scan_targets():
    import nmap
    nm = nmap.PortScanner()
    nm.scan('192.168.101.2-23,25-27', '1-9000')
    global scan = nm

def ssh_scan():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for network in targets:
            for service in network.services:
                if service.protocol is Protocol.SSH:
                    futures.append(executor.submit(ssh_to_host, service.parent))

def start_monitor():
    for network in targets:
        for port in network.ports:
            task = MonitorTask(network.ip, port)
            task.start()
            tasks.append(task)

interface = OrderedDict([
['Ingest model', import_ad],
['Run scans', scan_targets],
['Test SSH logins', ssh_scan],
['Record attack', None],
['Start monitoring hosts', start_monitor],
['Exit', exit]
])

def print_interface():
    for index, line in enumerate(interface.keys()):
        print("{}) {}".format(index, line))

print(header)
print_interface()

while(True):
    f, c = None, None
    try:
        c = int(input("> "))
    except ValueError:
        print("That doesn't look like a valid entry")
    if c:
        try:
            f = interface[list(interface.keys())[c]]
        except IndexError:
            print("That looks like it's out of range")
        if f:
            f()
