import asyncio
import random
from room import Room
from client import Client, ClientStatus, ClientRole
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK

# We use this variable to keep track of currently connected clients
connections_pool = set()

# Keep a list of available clients 
available_clients = set()

# A set to keep track of actively used rooms
rooms = set()

# Function to poll clients every 5 seconds and confirm their connection state to the server. (connected or not connected)
def handle_client_disconnection(disconnected_client):
            if disconnected_client.room:
                # Bring the other connected peer left in the room back to available pool
                for c in disconnected_client.room.clients:
                    if c != disconnected_client:
                        available_clients.add(c)
            # Clean up after client disconnection
            if disconnected_client.room in rooms:
                rooms.remove(disconnected_client.room)
                disconnected_client.room.close()
            if disconnected_client in available_clients:
                available_clients.remove(disconnected_client)
            if disconnected_client in connections_pool:
                connections_pool.remove(disconnected_client)

async def polling(client):
    while True:
        try:
            await client.conn.send("ping")
        except (ConnectionClosed, ConnectionClosedOK):
            print(f"{client.conn.id} closed the connection, removing from the pool")
            handle_client_disconnection(client)
            break
        await asyncio.sleep(1)

async def matchmake():
    while True:
        if len(available_clients) > 1:
            room = Room(1)
            client1 = random.choice(tuple(available_clients)) 
            available_clients.remove(client1)
            client2 = random.choice(tuple(available_clients))
            available_clients.remove(client2)

            if client1 in connections_pool:
                room.add(client1)
                room.add(client2)
                # Randomly match the newly connected client to another one and assign a role to each client a role for perfect negotiation
                # https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Perfect_negotiation 
                await client1.conn.send(f"ID: {client1.conn.id} Role: {ClientRole.POLITE.value} and matched with {client2.conn.id}")
                await client2.conn.send(f"ID: {client2.conn.id} Role: {ClientRole.IMPOLITE.value} and matched with {client1.conn.id}")
                # await matched_client.conn.send(ClientRole.POLITE.value)
                # await client.conn.send(ClientRole.IMPOLITE.value)
            # Add the room to the set of rooms
            rooms.add(room)
            print("Current rooms state: ", rooms)
        await asyncio.sleep(1)

async def handle_connections(conn):
    client = Client(conn, ClientStatus.AVAILABLE, None)
    print(f"New connection with UUID: {client.conn.id}, was added to the pool.")
    connections_pool.add(client)
    available_clients.add(client)
    await polling(client)

async def main():
    async with serve(handle_connections, "localhost", 8765) as server:
        await matchmake()
        await server.serve_forever()

if __name__ == "__main__":
    print("Websocket server is running on port 8765...")
    asyncio.run(main())
