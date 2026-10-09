import phonenumbers
from src.domain.value_objects.anonymized_span import AnonymizedSpan


class PhoneProcessor:
    def __init__(self, region: str = "RU") -> None:
        self._region = region

    def execute(self, text: str) -> list[AnonymizedSpan]:
        parts: list[AnonymizedSpan] = []
        for match in phonenumbers.PhoneNumberMatcher(text, self._region):
            parts.append(
                AnonymizedSpan(
                    predicted_type="phone",
                    original_value=text[match.start:match.end],
                    start=match.start,
                    end=match.end,
                )
            )
        return parts