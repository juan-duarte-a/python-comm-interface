import socket
import time
import threading


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
    input_comm_handler: threading.Thread
    OUTPUT_DATA_SIZE: int = 3
    INPUT_DATA_SIZE: int = 50
    state_parameters: dict

    def __init__(self, latency: float = 0.005, verbose_option: bool = False):
        self.output_port = 11435
        self.input_port = 11436
        self.connected = False
        self.start_timestamp = time.time()
        self.server_latency = latency
        self.verbose = verbose_option
        self.state_parameters = {
            "is_oriented": True,
            "distance_from_center": 0,
            "front_distance": 0,
            "track_completion": 0.0
        }

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

        print("Iniciando transmisión de datos por conexión de salida.")
        connection_check = self.send_action(self.CONNECTION_OK)
        if connection_check is not None and connection_check[0] == Errors.OK:
            print("Respuesta recibida en conexión de salida.")
        elif connection_check is not None and connection_check[0] == Errors.CONNECTION_ERROR:
            print("¡Error estableciendo conexión de salida!")
            return
        print("Conexión de salida establecida.")

        self.input_socket.bind(server_address_receive)
        self.input_socket.listen()

        while True:
            if self._connection_wait_completed():
                break
            print("Esperando conexión de entrada con ML Racing...")
            time.sleep(1.0)

        if len(self.client_address_receive) > 0:
            print("Conexión de entrada establecida.")
            print("Conexión con ML Racing completada.")
            self.connected = True
            self.input_comm_handler = threading.Thread(target=self._input_data_handler)
            self.input_comm_handler.start()
            time.sleep(0.6)
            if self.verbose:
                print("Continuando ejecución del hilo principal.")
        else:
            print("¡Error estableciendo conexión de entrada!")

    def communicate_test(self, iterations: int = 1) -> None:
        """
        Prueba la velocidad de conexión entre cliente y servidor.

        :param iterations:
            Cantidad de iteraciones a ejecutar.
        """
        data_sent: bytearray
        data_received: list
        for i in range(iterations):
            data_sent = bytearray(bytes([65, 66, 67]))
            if self.verbose:
                print("Iteración:", i)
            self.send_action(data_sent, True)

    def send_action(self, action: bytearray, response_test: bool = False) -> list:
        """
        Envía una acción al vehículo.

        :param action:
            Acción a ejecutar de acuerdo a las constantes definidas en la clase Actions de este módulo.
        :param response_test:
            Ejecuta el método en modo de prueba. Dejar en 'False' (valor por defecto) para uso normal.
        :return:
            'None', en modo normal.
            'list', en modo de prueba, con dos valores: código de error y resultado.
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
                print("Enviado ->", action.decode(), _message, "- Bytes:", bytes_sent)

            if response_test:
                data_received = bytes()
                while action != Actions.END and len(data_received) == 0:
                    data_received = self.output_socket.recv(self.OUTPUT_DATA_SIZE)
                    if len(data_received) == 0:
                        time.sleep(self.server_latency)

                result = [0, data_received]

                if self.verbose:
                    print("Recibido <-", data_received)
            time.sleep(self.server_latency)
        except AttributeError:
            result = Errors.get_error(Errors.CONNECTION_ERROR)
        finally:
            return result if response_test else None

    def close_comm(self) -> None:
        """
        Finaliza la conexión con ML Racing.
        """

        self.output_socket.close()
        self.input_socket.close()
        self.connected = False

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

    def _input_data_handler(self) -> None:
        message: str
        message_length: bytes
        data_received: bytes = bytes()
        parameters: list
        conn = self.client_address_receive[0]

        if self.verbose:
            print("Iniciando hilo secundario...")
        while len(data_received) == 0:
            data_received = conn.recv(self.INPUT_DATA_SIZE)

        if self.verbose:
            print("Transmisión de datos de conexión de entrada <-", data_received.decode())

        while self.connected:
            data_received = bytes()
            while len(data_received) == 0:
                message_length = conn.recv(1)
                data_received = conn.recv(message_length[0])
            message = data_received.decode()
            if data_received[0] == 76 and data_received[1] == 84:
                if self.verbose:
                    print("Recibido <-", data_received.decode())
            else:
                parameters = message.split(":")
                self.state_parameters["is_oriented"] = str(parameters[0]).lower() == "true"
                self.state_parameters["distance_from_center"] = int(parameters[1])
                self.state_parameters["front_distance"] = int(parameters[2])
                self.state_parameters["track_completion"] = float(parameters[3])
            time.sleep(self.server_latency * 2)
