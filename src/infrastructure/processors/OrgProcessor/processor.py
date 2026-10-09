from natasha import (Doc,
                     MorphVocab,
                     NewsEmbedding,
                     NewsNERTagger,
                     Segmenter)

from src.application.dto.income_message import IncomeMessageDTO
from src.domain.value_objects.anonymized_span import AnonymizedSpan


class OrgProcessor:
    def __init__(self) -> None:
        self._segmenter = Segmenter()
        self._morph_vocab = MorphVocab()
        self._ner_tagger = NewsNERTagger(NewsEmbedding())

    def execute(self, text: str) -> list[AnonymizedSpan]:
        doc = Doc(text)
        doc.segment(self._segmenter) # type: ignore
        doc.tag_ner(self._ner_tagger) # type: ignore

        parts: list[AnonymizedSpan] = []
        for span in doc.spans: # type: ignore
            if span.type != "ORG": # type: ignore
                continue
            span.normalize(self._morph_vocab) # type: ignore
            parts.append(
                AnonymizedSpan(
                    original_value=text[span.start:span.stop], # type: ignore
                    start=span.start, # type: ignore
                    end=span.stop, # type: ignore
                )
            )
        return parts
