from dataclasses import dataclass

@dataclass
class AnonymizedSpan:
    predicted_type: str
    original_value: str
    start: int
    end: int
