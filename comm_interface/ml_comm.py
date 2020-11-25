import socket
import time


class Actions:
    """
    Acciones para ser usadas como parámetros en el método 'send_action' de la clase CommInterface.
    """

    END = bytearray(bytes([65, 27, 4]))
    RUN = bytearray(bytes([65, 82, 78]))
    STOP = bytearray(bytes([65, 83, 84]))
    TURN_LEFT = bytearray(bytes([65, 84, 76]))
    TURN_RIGHT = bytearray(bytes([65, 84, 82]))


class Errors:
    """
    Clase con definición de errores usados en este módulo.
    """

    OK: int = 0
    DEFAULT_ERROR: int = 1
    CONNECTION_ERROR: int = 2
    BUSY: int = 3

    @staticmethod
    def get_error(err: int) -> list:
        """
        Método para uso interno del módulo.
        """

        return [err, None]


class CommInterface:
    """
    Controlador de comunicación entre Python y ML Racing.
    """

    CONNECTION_OK = bytearray(bytes([67, 79, 75]))
    CENTER_DISTANCE = bytearray(bytes([82, 67, 68]))
    IS_ORIENTED = bytearray(bytes([82, 73, 79]))
    BYTE_TRUE: int = 84
    BYTE_FALSE: int = 70

    output_socket: socket
    input_socket: socket
    output_port: int
    input_port: int
    client_address_receive: tuple
    connected: bool
    start_timestamp: float
    server_latency: float
    verbose: bool

    def __init__(self, latency: float = 0.005, verbose_option: bool = False):
        self.output_port = 11435
        self.connected = False
        self.start_timestamp = time.time()
        self.server_latency = latency
        self.verbose = verbose_option

    def connect(self, output_port_number: int = 11435, input_port_number: int = 11436) -> None:
        """
        Establece la conexión entre Python y ML Racing.

        :param output_port_number:
            Número del puerto en 'localhost' para conexión de salida a ML Racing.
            Valor por defecto: 11435.
        :param input_port_number:
            Número del puerto en 'localhost' para conexión de entrada de ML Racing.
            Valor por defecto: 11436.
        """

        connection_check: list

        self.output_port = output_port_number
        self.output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address_send: tuple = ('localhost', self.output_port)

        self.input_port = input_port_number
        self.input_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address_receive: tuple = ('localhost', self.input_port)

        while True:
            if self._connect_request_completed(server_address_send):
                break
            print("Esperando conexión de salida con ML Racing...")
            time.sleep(1.0)

        connection_check = self.send_action(self.CONNECTION_OK)
        if connection_check[0] == Errors.OK:
            print("Conexión de salida establecida.")
        elif connection_check[0] == Errors.CONNECTION_ERROR:
            print("¡Error estableciendo conexión de salida!")
            return

        self.input_socket.bind(server_address_receive)
        self.input_socket.listen()

        while True:
            if self._connection_wait_completed():
                break
            print("Esperando conexión de entrada con ML Racing...")
            time.sleep(1.0)

        if len(self.client_address_receive) > 0:
            self.connected = True
            print("Conexión de entrada establecida.")
            print("Conexión con ML Racing completada.")
        else:
            print("¡Error estableciendo conexión de entrada!")

    def _connect_request_completed(self, address: tuple) -> bool:
        try:
            self.output_socket.connect(address)
            return True
        except ConnectionRefusedError:
            return False

    def _connection_wait_completed(self) -> bool:
        try:
            self.client_address_receive = self.input_socket.accept()
            return True
        except ConnectionRefusedError:
            return False

    def _get_bool(self, data: bytes) -> bool:
        return True if data[2] == self.BYTE_TRUE else False

    @staticmethod
    def _get_int(data: bytes) -> int:
        if int(data[1] / 128) == 0:
            return -1 * (data[1] * 256 + data[2])
        else:
            return (data[1] - 128) * 256 + data[2]

    @staticmethod
    def _int_byte_code(int_value: int) -> list:
        int1: int
        int2: int

        int1 = int(abs(int_value) / 256)
        if int_value > 0:
            int1 += 128
        int2 = abs(int_value) - (int1 if int1 < 128 else (int1 - 128)) * 256

        return [int1, int2]

    def communicate_test(self, iterations: int = 1) -> None:
        """
        Prueba la velocidad de conexión entre cliente y servidor.

        :param iterations:
            Cantidad de iteraciones a ejecutar.
        """
        data_sent: bytearray
        data_received: list
        # Send data
        # input("Start [Enter] ") # Manual activation of the communication protocol.
        for i in range(iterations):
            data_sent = bytearray(bytes([65, 66, 67]))
            # data_sent.clear() # bytearray must be empty before sending it.
            # data_sent.extend(map(ord, data_string)) # str to bytearray.
            if self.verbose:
                print("Iteración:", i)
            self.send_action(data_sent)

    def distance_from_center(self) -> list:
        """
        Retorna la distancia a la que el vehículo se encuentra del centro de la pista.

        :return:
            'list' de dos valores: entero con el código de error y resultado.
            Si el vehículo se encuentra por fuera de la pista el resultado será 0.
        """

        result: list = self.send_action(self.CENTER_DISTANCE)
        distance: int

        if result[0] == Errors.OK:
            distance = self._get_int(result[1])
            return [Errors.OK, distance]
        elif result[0] == Errors.BUSY:
            return Errors.get_error(Errors.BUSY)
        else:
            return Errors.get_error(Errors.DEFAULT_ERROR)

    def is_oriented(self) -> list:
        """
        Verifica la orientación del vehículo de acuerdo al sentido de la pista.

        :return:
            'list' de dos valores: entero con el código de error y resultado.
            El resultado será True si el vehículo se encuentra correctamente orientado, False de lo contrario.
            Si el vehículo se encuentra por fuera de la pista el resultado será False.
        """

        result: list = self.send_action(self.IS_ORIENTED)
        oriented: bool

        if result[0] == Errors.OK:
            oriented = self._get_bool(result[1])
            return [Errors.OK, oriented]
        elif result[0] == Errors.BUSY:
            return Errors.get_error(Errors.BUSY)
        else:
            return Errors.get_error(Errors.DEFAULT_ERROR)

    def send_action(self, action: bytearray) -> list:
        """
        Envía una acción al vehículo.

        :param action:
            Acción a ejecutar de acuerdo a las constantes definidas en la clase Actions de este módulo.
        :return:
            'list' con dos valores: código de error y resultado.
        """

        result: list = []
        data_received: bytes
        _message: str = ""
        bytes_sent: int
        wait_time: float = time.time() - self.start_timestamp

        if wait_time < self.server_latency and self.connected:
            if self.verbose:
                print("Servidor de salida ocupado. - Err:", Errors.BUSY, "\nIntentando de nuevo...")
            time.sleep(self.server_latency - wait_time)
            # return Errors.get_error(Errors.BUSY)
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
        elif action == self.CENTER_DISTANCE:
            _message = "CENTER_DISTANCE"
        elif action == self.IS_ORIENTED:
            _message = "IS_ORIENTED"

        try:
            bytes_sent = self.output_socket.send(action)
            if self.verbose:
                print("Enviado ->", action.decode(), _message, "- bytes:", bytes_sent)

            data_received = bytes()
            while action != Actions.END and len(data_received) == 0:
                data_received = self.output_socket.recv(3)
                if len(data_received) == 0:
                    time.sleep(self.server_latency)
            result = [0, data_received]
            if self.verbose:
                print("Recibido <-", data_received)
        except AttributeError:
            result = Errors.get_error(Errors.CONNECTION_ERROR)
        finally:
            return result

    def close_comm(self) -> None:
        """
        Finaliza la conexión con ML Racing.
        """

        self.output_socket.close()
