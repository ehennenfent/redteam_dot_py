from collections import OrderedDict
import

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

def import_ad():
    global target
    from build_460_models import networks
    target = networks

def scan_targets():
    import nmap
    nm = nmap.PortScanner()
    nm.scan('192.168.101.2-23,25-27', '1-9000')


interface = OrderedDict([
['Ingest model', import_ad],
['Run scans', None],
['Ingest scans', None],
['Record attack', None],
['Start background tasks', None],
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
