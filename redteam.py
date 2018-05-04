from collections import OrderedDict
from tasks import MonitorTask
import concurrent.futures
import glob
import importlib.util
import pprint as pp

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

def import_from_filename(filename):
    spec = importlib.util.spec_from_file_location("attack_mod", filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def ingest_model():
    global targets
    engagements = glob.glob('data/engagements/*.py')
    for index, engagement in enumerate(engagements):
        print(index, " -- ", engagement)
    index = int(input("Select an engagement> "))
    ns = import_from_filename(engagements[index])
    targets = ns.networks
    print("imported {} targets".format(len(targets)))

def attack_all_hosts():
    attacks = glob.glob('attacks/*.py')
    for index, attack in enumerate(attacks):
        print(index, " -- ", attack)
    index = int(input("Select an attack> "))
    ns = import_from_filename(attacks[index])
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for network in targets:
            for host in network.hosts:
                futures.append(executor.submit(ns.attack, host))
        for future in concurrent.futures.as_completed(futures):
            print("Attack Complete")

#TODO: only works for NAT networks, not flat
def start_monitor():
    for network in targets:
        for port in network.ports:
            task = MonitorTask(network.get_host_by_port(port), network.ip, port)
            task.start()
            tasks.append(task)

interface = OrderedDict([
['Ingest model', ingest_model],
['Run attack on all hosts', attack_all_hosts],
['Start monitoring hosts', start_monitor],
['Print targets', lambda: pp.pprint(targets)],
['Print help', None],
['Exit', exit]
])

def print_interface():
    for index, line in enumerate(interface.keys()):
        print("{}) {}".format(index, line))

print(header)
print_interface()
interface['Print help'] = print_interface

while(True):
    f, c = None, None
    try:
        c = int(input("> "))
    except ValueError:
        print("That doesn't look like a valid entry")
    if c is not None:
        try:
            f = interface[list(interface.keys())[c]]
        except IndexError:
            print("That looks like it's out of range")
        if f:
            f()
