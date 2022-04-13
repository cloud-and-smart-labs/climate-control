import asyncio
import json
import os

import websockets


class Broker:
    def __init__(self, host="0.0.0.0", port=80) -> None:
        self._HOST = host
        self._PORT = port
        self._subscriber_connection = set()
        self._sensor_data = dict()

        asyncio.run(self._server())

    async def _server(self) -> None:
        async with websockets.serve(
            self._connection_handler,
            self._HOST,
            self._PORT,
            ping_interval=None,
        ):
            await asyncio.Future()

    async def _connection_handler(self, connection: websockets) -> None:

        try:
            message = await connection.recv()
            connection_type = json.loads(message)

        except websockets.ConnectionClosedOK:
            print("_connection_handler : Connection closed")
            return
        except Exception as e:
            print(f"_connection_handler : {e}")
            await connection.close()
            return

        if connection_type["type"] == Broker.ConnectionType.PUBLISH:
            print('Connection type : PUBLISH')
            await self.publisher(connection)

        elif connection_type["type"] == Broker.ConnectionType.SUBSCRIBE:
            print('Connection type : SUBSCRIBE')
            self._subscriber_connection.add(connection)
            await self.subscriber(connection)

        else:
            print('Connection type : UNKNOWN')
            connection.close()

    async def subscriber(self, subscriber_connection: websockets):
        try:
            async for message in subscriber_connection:
                print(f'subscriber : {message}')

        except websockets.ConnectionClosedOK:
            print('subscriber : Connection closed')
        except Exception as e:
            print('subscriber : {e}')
        finally:
            self._subscriber_connection.remove(subscriber_connection)

    async def publisher(self, publisher_connection: websockets):
        try:
            async for message in publisher_connection:
                current_data = (json.loads(message))

                for port in current_data.keys():
                    self._sensor_data[port] = current_data[port]

                print(self._sensor_data)
                websockets.broadcast(
                    self._subscriber_connection,
                    json.dumps(self._sensor_data)
                )

        except websockets.ConnectionClosedOK:
            print('publisher : Connection closed')
        except Exception as e:
            print(f'publisher : {e}')

    class ConnectionType:
        PUBLISH = 'publish'
        SUBSCRIBE = 'subscribe'


if __name__ == '__main__':

    PORT = 8080

    if "PORT" in os.environ:
        PORT = int(os.environ["PORT"])

    Broker(host='0.0.0.0', port=PORT)
