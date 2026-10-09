from urlextract import URLExtract # type: ignore
from src.domain.value_objects.anonymized_span import AnonymizedSpan


class UrlProcessor:
    def __init__(self) -> None:
        self._extractor = URLExtract() # type: ignore

    def execute(self, text: str) -> list[AnonymizedSpan]:
        parts: list[AnonymizedSpan] = []
        for url in self._extractor.find_urls(text): # type: ignore
            start = text.find(url) # type: ignore
            if start == -1:
                continue
            parts.append(
                AnonymizedSpan(
                    original_value=url, # type: ignore
                    start=start,
                    end=start + len(url), # type: ignore
                )
            )
        return parts
        