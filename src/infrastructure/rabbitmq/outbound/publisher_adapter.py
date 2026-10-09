from src.infrastructure.rabbitmq.adapters.publisher import RabbitMQPublisher
from src.application.dto.outbound_message import OutboundMessageDTO

class RabbitMQOutboundAdapter:
    def __init__(self,
                 publisher: RabbitMQPublisher) -> None:
        self._publisher = publisher

    def result_publish(self, message: OutboundMessageDTO) -> None:
        self._publisher.publish(message=message.body, routing_key="result")
