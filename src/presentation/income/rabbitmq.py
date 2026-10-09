from src.application.dto.income_message import IncomeMessageDTO
from src.application.use_cases.anonymize_message_use_case import AnonymizeMessageUseCase

class RabbitMQIncomeAdapter:
    def __init__(self,
                 anonymize_use_case: AnonymizeMessageUseCase) -> None:
        self._anonymize_use_case = anonymize_use_case

    def __call__(self, message: str) -> None:
        self._anonymize_use_case.anonymize(message=IncomeMessageDTO(message))
