from dataclasses import dataclass

@dataclass
class AnonymizedSpan:
    original_value: str
    start: int
    end: int
