from enum import Enum, auto

class OS(Enum):
    Windows = auto()
    Linux = auto()
    Other = auto()

class Arch(Enum):
    x86 = auto()
    x64 = auto()
    ARM = auto()
    MIPS = auto()
    Other = auto()

class Port(Enum):
    tcp = auto()
    udp = auto()