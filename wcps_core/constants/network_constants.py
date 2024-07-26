class InternalKeys:
    XOR_AUTH_SEND = 0x23
    XOR_GAME_SEND = 0xA3


class Ports:
    INTERNAL = 5012
    AUTH_CLIENT = 5330
    GAME_CLIENT = 5340
    UDP1 = 5350
    UDP2 = 5351

# A user with DEV rights will see every type of server.
# Admins and regular users will only see Entire/Adult types.
# Everyone will see trainee type servers

class ServerTypes:
    ENTIRE = 0
    ADULT = 1
    CLAN = 2
    EMPTY = 3
    TEST = 4
    DEVELOPMENT = 5
    NONE = 6
    TRAINEE = 21