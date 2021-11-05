from payment_package.adapters.repository import AbstractRepository as PaymentAbstractRepository
from payment_package.service_layer.payment_processor import AbstractPaymentProcessor
from payment_package.service_layer.payment_response import PaymentResponse, PaymentStatus
from payment_package.domain import model
from customer_package.adapters.repository import AbstractRepository as CustomerAbstractRepository


class FakeRepository(PaymentAbstractRepository):
    def __init__(self, payments):
        self._payments = set(payments)

    def add_payment(self, payment: model.Payment):
        self._payments.add(payment)

    def list_payments(self):
        return list(self._payments)


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


class FakePaymentProcessor(AbstractPaymentProcessor):

    def pay(self, amount, currency, card_number, card_exp_month, card_exp_year,
            card_cvc, payment_id=None) -> PaymentResponse:
        return PaymentResponse(payment_id=payment_id, status=PaymentStatus.SUCCEEDED,
                               msg='💰 Payment received!')


class FakeCustomerRepository(CustomerAbstractRepository):
    def __init__(self, customers):
        self._customers = set(customers)

    def add_customer(self, customer: model.Customer):
        self._customers.add(customer)

    def select_customer_by_reference(self, customer_ref) -> model.Customer:
        try:
            return next(c for c in self._customers if c.reference == customer_ref)
        except StopIteration:
            return None

    def select_customer_by_email(self, email) -> model.Customer:
        try:
            return next(c for c in self._customers if c.email == email)
        except StopIteration:
            return None
