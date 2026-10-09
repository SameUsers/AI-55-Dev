import re

from src.domain.value_objects.anonymized_span import AnonymizedSpan


class EmailProcessor:
    _EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    )
    def execute(self, text: str) -> list[AnonymizedSpan]:
        parts: list[AnonymizedSpan] = []
        for match in self._EMAIL_PATTERN.finditer(text):
            parts.append(
                AnonymizedSpan(
                    original_value=match.group(0),
                    start=match.start(),
                    end=match.end(),
                )
            )
        return parts
