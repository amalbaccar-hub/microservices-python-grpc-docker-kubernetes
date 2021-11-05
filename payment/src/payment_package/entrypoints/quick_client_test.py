import grpc
from payment_package.entrypoints.payment_service.payment_pb2_grpc import PaymentServiceStub
from payment_package.entrypoints.payment_service.payment_pb2 import *
import uuid


def randon_suffix():
    return uuid.uuid4().hex[:6]


def random_payment_ref():
    return f'payment-{randon_suffix()}'


def run():
    channel = grpc.insecure_channel("localhost:50053")
    client = PaymentServiceStub(channel)

    payment_request = PaymentRequest(
        payment=Payment(payment_ref=random_payment_ref(), customer_ref="customer-Stephanie Gansh-c07c30", amount=1500,
                        currency=eur, card_number='4242424242424242',
                        card_exp_month=5, card_exp_year=2025, card_cvc='189'))

    response = client.pay(payment_request)

    print(f'response status: {response.success}')
    print(f'response message: {response.message}')


if __name__ == "__main__":
    run()
