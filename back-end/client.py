from enum import Enum

class ClientStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

class ClientRole(Enum):
    POLITE = "polite"
    IMPOLITE = "impolite"

class Client:
    def __init__(self, conn, status, room):
        self.conn = conn
        self.status = status
        self.room = room

    def __str__(self):
        return self.conn.id
