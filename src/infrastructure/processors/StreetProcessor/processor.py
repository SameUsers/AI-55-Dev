from gliner import GLiNER

from src.domain.value_objects.anonymized_span import AnonymizedSpan


class AddressProcessor:
    def __init__(self) -> None:
        self._model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")

        self._window_size = 600

        self._label_to_type = {
            "address": "addr",
            "street address": "addr",
            "person": "en_name",
            "person name": "en_name",
            "organization": "org",
            "company": "org",
        }

    def execute(self, text: str) -> list[AnonymizedSpan]:
        if not text:
            return []

        spans: list[AnonymizedSpan] = []

        for offset in range(0, len(text), self._window_size):
            window = text[offset : offset + self._window_size]

            entities = self._model.predict_entities(
                window,
                labels=list(self._label_to_type.keys()),
                threshold=0.5,
            )

            for entity in entities:
                label = entity["label"].lower()

                predicted_type = self._label_to_type.get(label)

                if predicted_type is None:
                    continue

                start = offset + entity["start"]
                end = offset + entity["end"]

                if start >= end:
                    continue

                spans.append(
                    AnonymizedSpan(
                        predicted_type=predicted_type,
                        original_value=text[start:end],
                        start=start,
                        end=end,
                    )
                )

        return spans
