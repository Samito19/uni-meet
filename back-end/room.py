from client import ClientStatus

class Room:
    def __init__(self, id):
        self.id = id
        self.clients = set()

    def __str__(self):
        return f"room_id: {self.id} clients: {self.clients}"

    def add(self, client):
        client.status = ClientStatus.BUSY
        client.room = self
        self.clients.add(client)
    
    def close(self):
        for client in self.clients:
            client.room = None
            client.status = ClientStatus.AVAILABLE
