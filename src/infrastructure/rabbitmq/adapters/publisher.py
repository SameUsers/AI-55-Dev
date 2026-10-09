from pika import BasicProperties
from src.infrastructure.rabbitmq.connection import RabbitMQConnection

class RabbitMQPublisher:
    def __init__(self, connection: RabbitMQConnection) -> None:
        self._connection = connection

    def publish(self, message: str, routing_key: str) -> None:
        self._connection.channel.basic_publish(
            exchange="",
            routing_key=routing_key,
            body=message.encode("utf-8"),
            properties=BasicProperties(delivery_mode=2),
        )
