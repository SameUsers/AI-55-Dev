from typing import Protocol
from src.domain.value_objects.anonymized_span import AnonymizedSpan


class IProcessor(Protocol):
    def execute(self, text: str) -> list[AnonymizedSpan]: ...
