from typing import Protocol
from src.application.dto.outbound_message import OutboundMessageDTO

class IResultPublisher(Protocol):
    def result_publish(self, message: OutboundMessageDTO) -> None:
        ...
