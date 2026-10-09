from src.application.dto.income_message import IncomeMessageDTO
from src.application.dto.outbound_message import OutboundMessageDTO
from src.application.ports.result_publisher import IResultPublisher
from src.application.ports.processor import IProcessor
from src.domain.value_objects.anonymized_span import AnonymizedSpan

class AnonymizeMessageUseCase:
    def __init__(self,
                 publisher: IResultPublisher,
                 ru_name_processor: IProcessor,
                 en_name_processor: IProcessor,
                 email_processor: IProcessor,
                 phone_processor: IProcessor,
                 url_processor: IProcessor,
                 org_processor: IProcessor,
                 loc_processor: IProcessor,
                 addr_processor: IProcessor) -> None:
        self._publisher = publisher
        self._ru_name_processor = ru_name_processor
        self._en_name_processor = en_name_processor
        self._email_processor = email_processor
        self._phone_processor = phone_processor
        self._url_processor = url_processor
        self._org_processor = org_processor
        self._loc_processor = loc_processor
        self._addr_processor = addr_processor

    def get_ru_name_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._ru_name_processor.execute(text=message.body)

    def get_en_name_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._en_name_processor.execute(text=message.body)

    def get_email_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._email_processor.execute(text=message.body)

    def get_phone_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._phone_processor.execute(text=message.body)

    def get_url_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._url_processor.execute(text=message.body)

    def get_org_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._org_processor.execute(text=message.body)

    def get_loc_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._loc_processor.execute(text=message.body)

    def get_addr_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        return self._addr_processor.execute(text=message.body)

    def get_all_spans(self, message: IncomeMessageDTO) -> list[AnonymizedSpan]:
        ru_names_spans = self.get_ru_name_spans(message=message)
        en_names_spans = self.get_en_name_spans(message=message)
        email_spans = self.get_email_spans(message=message)
        phone_spans = self.get_phone_spans(message=message)
        url_spans = self.get_url_spans(message=message)
        org_spans = self.get_org_spans(message=message)
        loc_spans = self.get_loc_spans(message=message)
        en_addr_spans = self.get_addr_spans(message=message)
        return [*ru_names_spans, 
                *en_names_spans, 
                *email_spans,
                *phone_spans,
                *url_spans,
                *org_spans,
                *loc_spans,
                *en_addr_spans]


    def anonymize(self, message: IncomeMessageDTO) -> None:
        spans = self.get_all_spans(message=message)
        candidates = sorted(
            spans,
            key=lambda span: (
                -(span.end - span.start),
                span.start,
                span.end,
                span.predicted_type,
            ),
        )

        selected: list[AnonymizedSpan] = []

        for span in candidates:
            if not (0 <= span.start < span.end <= len(message.body)):
                raise ValueError(
                    f"Некорректные границы фрагмента: "
                    f"[{span.start}:{span.end}] {span.original_value!r}"
                )

            actual_value = message.body[span.start:span.end]
            if actual_value != span.original_value:
                raise ValueError(
                    f"Фрагмент не совпадает с текстом: "
                    f"[{span.start}:{span.end}], "
                    f"ожидалось {span.original_value!r}, "
                    f"получено {actual_value!r}"
                )

            overlaps = any(
                span.start < existing.end and existing.start < span.end
                for existing in selected
            )

            if not overlaps:
                selected.append(span)

        selected.sort(key=lambda span: (span.start, span.end))

        parts: list[str] = []
        cursor = 0

        for span in selected:
            parts.append(message.body[cursor:span.start])
            parts.append(f"[[{span.predicted_type}]]")
            cursor = span.end

        parts.append(message.body[cursor:])
        anonymized_body = "".join(parts)

        self._publisher.result_publish(
            message=OutboundMessageDTO(body=anonymized_body)
        )
