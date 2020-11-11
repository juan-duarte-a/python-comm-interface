import socket
import time


class Actions:
    END = bytearray(bytes([27, 27, 27]))
    RUN = bytearray(bytes([48, 48, 48]))
    STOP = bytearray(bytes([49, 49, 49]))
    TURN_LEFT = bytearray(bytes([50, 50, 50]))
    TURN_RIGHT = bytearray(bytes([51, 51, 51]))


class CommInterface:
    sock: socket
    port: int = 11435
    connected: bool = False

    ERROR: list = ["Connection error!"]

    def connect(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address: tuple = ('localhost', self.port)

        while True:
            if self._connect_request_completed(server_address):
                break
            print("Waiting connection with server...")
            time.sleep(1.0)

        self.connected = True

    def _connect_request_completed(self, address: tuple) -> bool:
        try:
            self.sock.connect(address)
            return True
        except ConnectionRefusedError:
            return False

    @staticmethod
    def _get_distance(data: bytes) -> int:
        distance: int = data[1] * 256 + data[2]
        return distance

    def communicate_test(self, iterations: int = 1):
        data_sent: bytearray
        data_received: list
        # Send data
        # input("Start [Enter] ") # Manual activation of the communication protocol.
        for i in range(iterations):
            data_sent = bytearray(bytes([65, 66, 67]))
            # data_sent.clear() # bytearray must be empty before sending it.
            # data_sent.extend(map(ord, data_string)) # str to bytearray.
            print("Iteration:", i)
            self.send_action(data_sent)

    def send_action(self, action) -> list:
        result: list = []
        data_received: bytes
        _message: str = ""

        if action == Actions.RUN:
            _message = "RUN"
        elif action == Actions.STOP:
            _message = "STOP"
        elif action == Actions.TURN_LEFT:
            _message = "TURN_LEFT"
        elif action == Actions.TURN_RIGHT:
            _message = "TURN_RIGHT"

        try:
            self.sock.send(action)
            print("Sent:", action.decode(), _message)

            data_received = bytes()
            while action != Actions.END and len(data_received) == 0:
                data_received = self.sock.recv(3)
                result = [0, data_received]
                print("Received:", data_received)
                print("Front distance:", self._get_distance(data_received))

        except AttributeError:
            result = self.ERROR
        finally:
            return result

    def close_comm(self):
        self.sock.close()
