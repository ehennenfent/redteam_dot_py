from collections import OrderedDict

header = """
_________________________________________
           _ _
 ___ ___ _| | |_ ___ ___ _____   ___ _ _
|  _| -_| . |  _| -_| .'|     |_| . | | |
|_| |___|___|_| |___|__,|_|_|_|_|  _|_  |
                                |_| |___|
_________________________________________
"""

interface = OrderedDict([
['Ingest model', None],
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