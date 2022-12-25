from enum import Enum 

class InternalKeys(Enum):
    xOrKeyInternalSend = 0x23
    xOrKeyInternalRecieve = 0xA3


class Ports(Enum):
    internal = 5012
    authClient = 5330,
    gameClient = 5340,
    peerUDP1 = 5350,
    peerUDP2 = 5351

