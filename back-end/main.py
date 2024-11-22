import asyncio
import websockets
from websockets.asyncio.server import serve


connections_pool = set()

async def handle_connections(ws_conn):
    connections_pool.add(ws_conn)
    print(f"New connection with UUID: {ws_conn.id}, was added to the pool.")
    print("Pool: ", connections_pool)
    async for message in ws_conn:
        try:
            await ws_conn.send(f"You said: {message}")
        except websockets.exceptions.ConnectionClosed:
            print(f"{ws_conn.id} closed the connection, removing from the pool")
            connections_pool.remove(ws_conn)
            print("Pool: ", connections_pool)

async def main():
    async with serve(handle_connections, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    print("Websocket server is running on port 8765...")
    asyncio.run(main())

