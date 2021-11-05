import unittest
import payment_package.service_layer.services as services
from payment.tests.unit.fake_dependencies import FakeRepository, FakeSession, FakePaymentProcessor, \
    FakeCustomerRepository
from payment.tests.common_fixture import *
from customer_package.domain.model import Customer


class TestServices(unittest.TestCase):
    def setUp(self) -> None:
        self.customer_repo = FakeCustomerRepository([])
        self.payment_repo = FakeRepository([])
        self.session = FakeSession()
        self.payment_proc = FakePaymentProcessor()

    def tearDown(self) -> None:
        pass

    def test_pay(self):
        # triple A method
        # 1. arrange
        payment_ref = random_payment_ref()
        customer_ref = random_customer_ref('Antonio')
        self.customer_repo.add_customer(Customer(customer_ref, 'Antonio adolfo', 'antonio.adolfo@gmail.com'))

        # 2.act
        services.pay(payment_ref, customer_ref, 735, 'eur', '4242424242424242', 6, 2025, '567',
                     self.payment_repo, self.session, self.payment_proc)

        # 3.assert
        self.assertEqual(len(self.payment_repo.list_payments()), 1)
        self.assertEqual(self.session.commited, True)

    def test_error_for_customer_not_found(self):
        customer_ref = random_customer_ref()
        payment_ref = random_payment_ref()
        with self.assertRaises(services.CustomerNotFoundException) as context:
            services.pay(payment_ref, customer_ref,
                         1500, 'eur',
                         '5878397214141414',
                         2, 2026, '167', self.payment_repo, self.session,
                         self.payment_proc)

        res = None
        try:
            res = next(p for p in self.payment_repo.list_payments() if p.reference == payment_ref)
        except StopIteration:
            res = None

        self.assertTrue(f'customer with reference {customer_ref} not found' in str(context.exception))
        self.assertEqual(res, None)
        self.assertEqual(self.session.commited, False)

    def test_error_for_currency_not_supported(self):
        customer_ref = random_customer_ref('Jonas')
        _customer = Customer(customer_ref, 'Jonas', 'jonas.golf@gmail.com')
        self.repo.add_customer(_customer)
        payment_ref = random_payment_ref()
        currency = 'jhg'
        with self.assertRaises(services.CurrencyNotSupportedException) as context:
            services.pay(payment_ref, customer_ref,
                         1500, currency,
                         '5878397214141414',
                         2, 2026, '167', self.payment_repo, self.session,
                         self.payment_proc)

        res = None
        try:
            res = next(p for p in self.payment_repo.list_payments() if p.reference == payment_ref)
        except StopIteration:
            res = None

        self.assertTrue(f'given currency {currency} is not supported' in str(context.exception))
        self.assertEqual(res, None)
        self.assertEqual(self.session.commited, False)


if __name__ == '__main__':
    unittest.main()
