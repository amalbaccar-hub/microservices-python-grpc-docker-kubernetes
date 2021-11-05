from payment_package.domain import model
from payment_package.adapters.repository import AbstractRepository
from payment_package.service_layer.payment_processor import AbstractPaymentProcessor
from payment_package.service_layer.currency import Currency
from payment_package.service_layer.payment_response import PaymentStatus
from payment_package.entrypoints.customer_service.customer_registration_pb2 import *
from payment_package.entrypoints.customer_service.customer_registration_pb2_grpc import CustomerRegistrationStub
import grpc
from payment_package import config
import os

accepted_currencies = [Currency.EUR.value, Currency.GBP.value, Currency.USD.value]


class CustomerNotFoundException(Exception):
    pass


class CurrencyNotSupportedException(Exception):
    pass


class PaymentErrorException(Exception):
    pass


customer_host = os.getenv("CUSTOMER_HOST", "localhost")
customer_registration_channel = grpc.insecure_channel(f"{customer_host}:50051")
customer_registration_client = CustomerRegistrationStub(customer_registration_channel)


def pay(payment_ref, customer_ref, amount, currency, card_number, card_exp_month, card_exp_year, card_cvc,
        repo: AbstractRepository, session, payment_processor: AbstractPaymentProcessor):
    # Does customer exists if not throw
    customer_response = customer_registration_client.get_customer_by_reference(
        GetCustomerByReferenceRequest(customer_ref=customer_ref))
    if not customer_response.found:
        raise CustomerNotFoundException(f'customer with reference {customer_ref} not found')

    # do we support the currency if not throw
    if currency not in accepted_currencies:
        raise CurrencyNotSupportedException(f'given currency {currency} is not supported')

    # make the payment
    # stripe accepts lowercase currencies
    response = payment_processor.pay(amount, currency, card_number, card_exp_month,
                                     card_exp_year, card_cvc)

    # check the status, if not succeeded throw
    if response.status == PaymentStatus.ERROR:
        raise PaymentErrorException(f'Payment not received. Card not debited for customer: {customer_ref}. '
                                    f'error details= {response.message}')

    # insert the payment
    new_payment = model.Payment(response.payment_id, payment_ref, customer_ref, amount, currency, card_number,
                                card_exp_month,
                                card_exp_year,
                                card_cvc)
    repo.add_payment(new_payment)
    # TODO use grpc to allocate new_payment for the customer
    session.commit()

    # TODO send invoice or email confirmation
