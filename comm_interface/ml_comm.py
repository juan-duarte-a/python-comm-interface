import socket
import time


# Action constants to be passed as parameter to send_action method of CommInterface class.
class Actions:
    END = bytearray(bytes([65, 27, 4]))
    RUN = bytearray(bytes([65, 82, 78]))
    STOP = bytearray(bytes([65, 83, 84]))
    TURN_LEFT = bytearray(bytes([65, 84, 76]))
    TURN_RIGHT = bytearray(bytes([65, 84, 82]))


# Request constants to be passed as internal parameter to CommInterface class methods.
class Requests:
    CENTER_DISTANCE = bytearray(bytes([82, 67, 68]))
    IS_ORIENTED = bytearray(bytes([82, 73, 79]))


# Class with error definitions used in this module.
class Errors:
    CONNECTION_ERROR: int = 1
    BUSY: int = 2

    @staticmethod
    def get_error(err: int) -> list:
        return [err, list()]


# Communication handler between Python app and ml_racing game.
class CommInterface:
    sock: socket
    port: int
    connected: bool
    start_timestamp: float
    server_latency: float

    def __init__(self, latency: float = 0.005):
        self.port = 11435
        self.connected = False
        self.start_timestamp = time.time()
        self.server_latency = latency

    def connect(self, port_number: int = 11435):
        self.port = port_number
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    def _get_bool(data: bytes) -> bool:
        return True if data[2] == 84 else False

    @staticmethod
    def _get_int(data: bytes) -> int:
        return data[1] * 256 + data[2]

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

    def distance_from_center(self) -> int:
        result: list = self.send_action(Requests.CENTER_DISTANCE)

        if result[0] == 0:
            return self._get_int(result[1])

    def is_oriented(self) -> bool:
        result: list = self.send_action(Requests.IS_ORIENTED)

        if result[0] == 0:
            return self._get_bool(result[1])

    def send_action(self, action) -> list:
        result: list = []
        data_received: bytes
        _message: str = ""
        bytes_sent: int

        # print(time.time() - self.start_timestamp, self.start_timestamp)
        if time.time() - self.start_timestamp < self.server_latency:
            print("Server busy - Err:", Errors.BUSY)
            return Errors.get_error(Errors.BUSY)
        else:
            self.start_timestamp = time.time()

        if action == Actions.RUN:
            _message = "RUN"
        elif action == Actions.STOP:
            _message = "STOP"
        elif action == Actions.TURN_LEFT:
            _message = "TURN_LEFT"
        elif action == Actions.TURN_RIGHT:
            _message = "TURN_RIGHT"
        elif action == Requests.CENTER_DISTANCE:
            _message = "CENTER_DISTANCE"

        try:
            bytes_sent = self.sock.send(action)
            print("Sent:", action.decode(), _message, "- bytes:", bytes_sent)

            data_received = bytes()
            while action != Actions.END and len(data_received) == 0:
                data_received = self.sock.recv(3)
                if len(data_received) == 0:
                    time.sleep(self.server_latency)
                # print("Len data:", len(data_received))
            result = [0, data_received]
            print("Received:", data_received)
        except AttributeError:
            result = Errors.get_error(Errors.CONNECTION_ERROR)
        finally:
            return result

    def close_comm(self):
        self.sock.close()
