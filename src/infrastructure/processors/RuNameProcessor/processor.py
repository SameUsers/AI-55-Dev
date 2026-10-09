from natasha import (Doc, # type: ignore
                     MorphVocab,
                     NamesExtractor,
                     NewsEmbedding,
                     NewsNERTagger,
                     Segmenter)

from src.domain.value_objects.anonymized_span import AnonymizedSpan


class RuNameProcessor:
    def __init__(self) -> None:
        self._segmenter = Segmenter()
        self._morph_vocab = MorphVocab()
        self._ner_tagger = NewsNERTagger(NewsEmbedding())
        self._names_extractor = NamesExtractor(self._morph_vocab)

    def execute(self, text: str) -> list[AnonymizedSpan]:
        doc = Doc(text)
        doc.segment(self._segmenter) # type: ignore
        doc.tag_ner(self._ner_tagger) # type: ignore
        anonymized_parts: list[AnonymizedSpan] = []
        for span in doc.spans: # type: ignore
            if span.type != "PER": # type: ignore
                continue
            span.normalize(self._morph_vocab) # type: ignore
            span.extract_fact(self._names_extractor) # type: ignore
            anonymized_parts.append(
                AnonymizedSpan(
                    original_value=text[span.start:span.stop], # type: ignore
                    start=span.start, # type: ignore
                    end=span.stop, # type: ignore
                )
            )
        return anonymized_parts
