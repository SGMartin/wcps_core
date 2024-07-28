class ErrorCodes:
    SUCCESS = 1
    UPDATE = 2
    END_CONNECTION = 3
    INVALID_SERVER_TYPE = 4
    INVALID_KEY_SESSION = 0x100
    INVALID_SESSION_MATCH = 0x110
    ALREADY_AUTHORIZED = 0x120
    SERVER_LIMIT_REACHED = 0x130
    SERVER_NAME_USED = 0x140
    SERVER_ERROR_OTHER = 0x150

class UserRights:
    Blocked = 0
    Regular = 1
    Administrator = 3
    Developer = 5


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