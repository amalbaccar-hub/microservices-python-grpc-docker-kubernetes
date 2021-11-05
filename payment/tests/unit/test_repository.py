import unittest
from sqlalchemy import create_engine
from payment_package.adapters.orm import metadata, start_mappers
from sqlalchemy.orm import sessionmaker, clear_mappers
from payment_package.adapters.repository import SqlAlchemyRepository
from payment_package.domain.model import Payment
from payment.tests.common_fixture import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # we will be using in-memory db for the purpose of this test
        engine = create_engine('sqlite:///:memory:')
        metadata.create_all(engine)
        start_mappers()
        self.session = sessionmaker(bind=engine)()
        # repo is the under test component
        self.under_test = SqlAlchemyRepository(self.session)

    def tearDown(self) -> None:
        clear_mappers()

    @staticmethod
    def insert_payment(session, payment_id, customer_id):
        session.execute(
            "INSERT INTO payments (id, reference, customer_ref, amount, currency, card_number, card_exp_month, card_exp_year, card_cvc)"
            " VALUES (:id, :ref, :customer_ref, :amount, :currency, :card_number, :card_exp_month, :card_exp_year, :card_cvc)",
            dict(id=payment_id, ref='payment1', customer_ref=customer_id, amount=1500, currency='usd',
                 card_number='4242424242424242',
                 card_exp_month=5, card_exp_year=2026, card_cvc='673')
        )

    def test_repository_can_save_payment(self):
        _payment_id = random_payment_ref()
        _payment_ref = random_payment_ref('pay1')
        _customer_ref = random_customer_ref()
        _payment = Payment(_payment_id, _payment_ref, _customer_ref, 780, 'usd',
                           '4242424242424242', 6, 2026, '287')

        self.under_test.add_payment(_payment)
        self.session.commit()

        rows = self.session.execute('SELECT * FROM "payments"')

        self.assertEqual(list(rows),
                         [(_payment_id, _payment_ref, _customer_ref, 780, 'usd', '4242424242424242', 6, 2026, '287')])

    # TODO: add test for retrieving a payment


if __name__ == '__main__':
    unittest.main()
