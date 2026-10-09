from src.infrastructure.rabbitmq.connection import RabbitMQConnection
from src.infrastructure.rabbitmq.adapters.consumer import RabbitMQConsumer
from src.infrastructure.rabbitmq.adapters.publisher import RabbitMQPublisher
from src.presentation.income.rabbitmq import RabbitMQIncomeAdapter
from src.application.use_cases.anonymize_message_use_case import AnonymizeMessageUseCase
from src.infrastructure.rabbitmq.outbound.publisher_adapter import RabbitMQOutboundAdapter
from src.infrastructure.processors.RuNameProcessor.processor import RuNameProcessor
from src.infrastructure.processors.EnNameProcessor.processor import EnNameProcessor
from src.infrastructure.processors.EmailProcessor.processor import EmailProcessor
from src.infrastructure.processors.PhoneProcessor.processor import PhoneProcessor
from src.infrastructure.processors.UrlProcessor.processor import UrlProcessor
from src.infrastructure.processors.OrgProcessor.processor import OrgProcessor
from src.infrastructure.processors.LocProcessor.processor import LocationProcessor
from src.infrastructure.processors.StreetProcessor.processor import AddressProcessor

def main():
    rq_connection = RabbitMQConnection()
    rq_connection.connect()
    rq_consumer = RabbitMQConsumer(connection=rq_connection)
    rq_publisher = RabbitMQPublisher(connection=rq_connection)
    rq_publisher_adapter = RabbitMQOutboundAdapter(publisher=rq_publisher)

    ru_name_processor = RuNameProcessor()
    en_name_processor = EnNameProcessor()
    email_processor = EmailProcessor()
    phone_processor = PhoneProcessor()
    url_processor = UrlProcessor()
    org_processor = OrgProcessor()
    loc_processor = LocationProcessor()
    address_processor = AddressProcessor()

    anonymize_use_case = AnonymizeMessageUseCase(publisher=rq_publisher_adapter,
                                                 ru_name_processor=ru_name_processor,
                                                 en_name_processor=en_name_processor,
                                                 email_processor=email_processor,
                                                 phone_processor=phone_processor,
                                                 url_processor=url_processor,
                                                 org_processor=org_processor,
                                                 loc_processor=loc_processor,
                                                 addr_processor=address_processor)
    
    rq_income_handler = RabbitMQIncomeAdapter(anonymize_use_case=anonymize_use_case)
    rq_consumer.consume(handler=rq_income_handler)

main()