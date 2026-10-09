from collections.abc import Callable

from ..connection import RabbitMQConnection


class RabbitMQConsumer:
    def __init__(self, connection: RabbitMQConnection) -> None:
        self._connection = connection

    def consume(self, handler: Callable[[str], None]) -> None:
        channel = self._connection.channel
        try:
            for method, properties, body in channel.consume(self._connection.queue_name, inactivity_timeout=1): # type: ignore
                if method is None:
                    continue
                if body is None:
                    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    continue
                try:
                    _body = body.decode("utf-8")
                    message = _body
                except Exception:
                    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    continue
                try:
                    handler(message)
                except Exception:
                    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    raise Exception
                channel.basic_ack(delivery_tag=method.delivery_tag)
        finally:
            channel.cancel()
