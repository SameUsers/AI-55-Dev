from natasha import AddrExtractor, MorphVocab # type: ignore
from src.domain.value_objects.anonymized_span import AnonymizedSpan


class RuAddressProcessor:
    def __init__(self) -> None:
        self._morph_vocab = MorphVocab()
        self._addr_extractor = AddrExtractor(self._morph_vocab)

    def execute(self, text: str) -> list[AnonymizedSpan]:
        match = self._addr_extractor.find(text) # type: ignore
        if not match:
            return []

        return [
            AnonymizedSpan(
                original_value=text[match.start:match.stop], # type: ignore
                start=match.start, # type: ignore
                end=match.stop, # type: ignore
            )
        ]
