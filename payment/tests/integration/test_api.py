import unittest
from payment.tests.common_fixture import *
from payment_package.entrypoints.customer_service.customer_registration_pb2 import *
from payment_package.entrypoints.customer_service.customer_registration_pb2_grpc import CustomerRegistrationStub
import payment_package.entrypoints.customer_service.customer_registration_pb2_grpc as customer_registration_pb2_grpc
import grpc
from payment_package.entrypoints.payment_service.payment_pb2 import *
import payment_package.entrypoints.payment_service.payment_pb2_grpc as payment_pb2_grpc
from payment_package.entrypoints.payment_service.payment_pb2_grpc import PaymentServiceStub
from payment_package.entrypoints.payment_grpc_controller import PaymentController
from payment.tests.integration import e2e_fixture
from sqlalchemy import create_engine
import payment_package.config as config_payment
import customer_package.config as config_customer
from payment_package.adapters.orm import metadata as metadata_payment
from customer_package.adapters.orm import metadata as metadata_customer
from customer_package.entrypoints.customer_registration_grpc_controller import CustomerRegistration
from sqlalchemy.orm import sessionmaker, clear_mappers
from concurrent import futures


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        # setup stuff is only needed when tests are run locally (with docker or kubernetes isn't needed)
        # create postgres db
        payment_engine = create_engine(config_payment.get_postgres_uri())
        e2e_fixture.wait_for_postgres_to_come_up(payment_engine)
        metadata_payment.create_all(payment_engine)

        # create postgres session
        session_payment = sessionmaker(bind=payment_engine)()

        # create postgres db
        customer_engine = create_engine(config_customer.get_postgres_uri())
        e2e_fixture.wait_for_postgres_to_come_up(customer_engine)
        metadata_customer.create_all(customer_engine)

        # create postgres session
        session_customer = sessionmaker(bind=customer_engine)()

        # start payment grpc payment_server
        self.payment_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentController(session_payment),
                                                              self.payment_server)
        self.payment_server.add_insecure_port(f'[::]:{config_payment.payment_grpc_port}')
        self.payment_server.start()

        # start customer registration grpc server
        self.customer_registration_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        customer_registration_pb2_grpc.add_CustomerRegistrationServicer_to_server(
            CustomerRegistration(session_customer),
            self.customer_registration_server)
        self.customer_registration_server.add_insecure_port(f'[::]:{config_customer.grpc_port}')
        self.customer_registration_server.start()

    def tearDown(self) -> None:
        # TODO: delete added items in db. we should bring db to initial state
        # TODO: add endpoints for deleting _customers and payments
        clear_mappers()
        self.customer_registration_server.stop(None)
        self.payment_server.stop(None)

    def test_happy_path_returns_success_payment_received_and_created(self):
        # triple A method
        # 1.arrange
        # given a customer
        _customer_ref = random_customer_ref('Maria')
        customer_registration_request = CustomerRegistrationRequest(
            Customer(customer_ref=_customer_ref, name='Maria Mercedes', email='maria.mercedes@gmail.com'))
        # register
        channel = grpc.insecure_channel('localhost:50051')
        customer_registration_stub = CustomerRegistrationStub(channel)
        customer_registration_result = customer_registration_stub.register_new_customer(customer_registration_request)

        # and payment request data
        _payment_ref = random_payment_ref()
        payment_request = PaymentRequest(
            Payment(payment_ref=_payment_ref, customer_ref=_customer_ref, amount=2800, currency=eur,
                    card_number='4242424242424242', card_exp_month=9, card_exp_year=2024, card_cvc='674'))

        # 2. act
        # pay
        payment_channel = grpc.insecure_channel('localhost:50053')
        payment_stub = PaymentServiceStub(payment_channel)
        payment_result = payment_stub.pay(payment_request)

        # 3. assert
        # both customer registration and payment requests passed
        self.assertEqual(customer_registration_result.success, True)
        self.assertEqual(customer_registration_result.message,
                         f'{str(customer_registration_request)} is now registered!')

        self.assertEqual(payment_result.success, True)
        self.assertEqual(payment_result.message, f'💰 Payment received for customer ref= {_customer_ref}')

        # check that payment is stored in db
        # TODO: Do not use repository instead create an endpoint to retrieve payments for _customers

    def test_unhappy_path_returns_failure_for_customer_not_found(self):
        # given a customer
        _customer_ref = random_customer_ref('Maria')

        # and payment request data
        _payment_ref = random_payment_ref()
        payment_request = PaymentRequest(
            Payment(payment_ref=_payment_ref, customer_ref=_customer_ref, amount=2800, currency=eur,
                    card_number='4242424242424242', card_exp_month=9, card_exp_year=2024, card_cvc='674'))

        # 2. act
        # pay
        payment_channel = grpc.insecure_channel('localhost:50053')
        payment_stub = PaymentServiceStub(payment_channel)
        payment_result = payment_stub.pay(payment_request)

        # 3. assert
        self.assertEqual(payment_result.success, False)
        self.assertEqual(payment_result.message, f'customer with reference {_customer_ref} not found')
