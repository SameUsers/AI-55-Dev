from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from pika import PlainCredentials, ConnectionParameters


class RabbitMQConnection:
    def __init__(self,
                 host: str = "localhost",
                 port: int = 5672,
                 username: str = "guest",
                 password: str = "guest",
                 virtual_host: str = "/",
                 queue_name: str = "default",
                 result_queue_name: str = "result") -> None:
        self._host: str = host
        self._port: int = port
        self._username: str = username
        self._password: str = password
        self._virtual_host: str = virtual_host
        self._queue_name: str = queue_name
        self._result_queue_name: str = result_queue_name
        self._credentials: PlainCredentials | None = None
        self._connection_parameters: ConnectionParameters | None = None
        self._connection: BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    def _create_credentials(self) -> None:
        self._credentials = PlainCredentials(username=self._username, password=self._password)

    def _create_connection_parameters(self) -> None:
        if self._credentials is None:
            raise RuntimeError()
        self._connection_parameters = ConnectionParameters(host=self._host,
                                                           port=self._port,
                                                           credentials=self._credentials,
                                                           virtual_host=self._virtual_host)

    def _create_connection(self) -> None:
        if self._connection_parameters is None:
            raise RuntimeError()
        self._connection = BlockingConnection(parameters=self._connection_parameters)

    def _create_channel(self) -> None:
        if self._connection is None:
            raise RuntimeError()
        self._channel = self._connection.channel()

    def _declare_income_queue(self) -> None:
        if self._channel is None:
            raise RuntimeError()
        self._channel.queue_declare(queue=self._queue_name, durable=True)

    def _declare_result_queue(self) -> None:
        if self._channel is None:
            raise RuntimeError()
        self._channel.queue_declare(queue=self._result_queue_name, durable=True)

    def connect(self) -> None:
        self._create_credentials()
        self._create_connection_parameters()
        self._create_connection()
        self._create_channel()
        self._declare_income_queue()
        self._declare_result_queue()

    @property
    def channel(self) -> BlockingChannel:
        if not self._channel:
            raise RuntimeError()
        return self._channel

    @property
    def queue_name(self) -> str:
        return self._queue_name

    @property
    def result_queue(self) -> str:
        return self._result_queue_name
