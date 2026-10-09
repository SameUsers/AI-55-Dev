from natasha import (Doc,
                     MorphVocab,
                     NewsEmbedding,
                     NewsNERTagger,
                     Segmenter)

from src.domain.value_objects.anonymized_span import AnonymizedSpan


class LocationProcessor:
    """Извлекает локации (LOC) из текста с помощью Natasha."""

    def __init__(self) -> None:
        self._segmenter = Segmenter()
        self._morph_vocab = MorphVocab()
        self._ner_tagger = NewsNERTagger(NewsEmbedding())

    def execute(self, text: str) -> list[AnonymizedSpan]:
        doc = Doc(text)
        doc.segment(self._segmenter)
        doc.tag_ner(self._ner_tagger)

        parts: list[AnonymizedSpan] = []
        for span in doc.spans:
            if span.type != "LOC":
                continue
            span.normalize(self._morph_vocab)
            parts.append(
                AnonymizedSpan(
                    original_value=text[span.start:span.stop],
                    start=span.start,
                    end=span.stop,
                )
            )
        return parts
