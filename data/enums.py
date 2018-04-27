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

class PortType(Enum):
    TCP = auto()
    UDP = auto()

class Protocol(Enum):
    SSH = auto()
    FTP = auto()
    DNS = auto()
    HTTP = auto()
    RDP = auto()
    XMPP = auto()
    SQL = auto()
    OTHER = auto()
