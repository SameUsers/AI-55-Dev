import spacy

from src.domain.value_objects.anonymized_span import AnonymizedSpan


class EnNameProcessor:
    def __init__(self, model: str = "xx_ent_wiki_sm") -> None:
        self._nlp = spacy.load(model)

    def execute(self, text: str) -> list[AnonymizedSpan]:
        doc = self._nlp(text)
        parts: list[AnonymizedSpan] = []
        for ent in doc.ents:
            if ent.label_ != "PERSON":
                continue
            parts.append(
                AnonymizedSpan(
                    predicted_type="en_name",
                    original_value=ent.text,
                    start=ent.start_char,
                    end=ent.end_char,
                )
            )
        return parts
