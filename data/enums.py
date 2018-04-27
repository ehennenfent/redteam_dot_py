from enum import Enum, auto

class OS(Enum):
    Windows = "Windows"
    Linux = "Linux"
    Other = "Other"

class Arch(Enum):
    x86 = "x86"
    x64 = "x64"
    ARM = "ARM"
    MIPS = "MIPS"
    Other = "Other"

class Protocol(Enum):
    SSH = "SSH"
    FTP = "FTP"
    DNS = "DNS"
    HTTP = "HTTP"
    RDP = "RDP"
    XMPP = "XMPP"
    SQL = "SQL"
    OTHER = "OTHER"
