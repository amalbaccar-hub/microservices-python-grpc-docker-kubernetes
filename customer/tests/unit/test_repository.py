import unittest
from sqlalchemy import create_engine
from customer_package.adapters.orm import metadata, start_mappers
from sqlalchemy.orm import sessionmaker, clear_mappers
from customer_package.adapters.repository import SqlAlchemyRepository
from customer_package.domain import model
import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_customer_ref(name=""):
    return f'customer-{name}-{random_suffix()}'


class TestRepository(unittest.TestCase):

    def setUp(self) -> None:
        engine = create_engine('sqlite:///:memory:')
        metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()
        self.under_test = SqlAlchemyRepository(self.session)

    def tearDown(self) -> None:
        clear_mappers()

    def test_repo_can_save_customer(self):
        _customer_ref = random_customer_ref('Maria Mercedes')
        _customer = model.Customer(_customer_ref, 'Maria Mercedes', 'maria.mercedes@gmail.com')

        self.under_test.add_customer(_customer)
        self.session.commit()

        rows = self.session.execute('SELECT * FROM customers WHERE reference=:ref', dict(ref=_customer_ref))
        self.assertEqual(len(rows), 1)

    @staticmethod
    def insert_customer(session, customer_id, customer_ref, name, email):
        session.execute(
            "INSERT INTO customers (id, reference, name, email)"
            " VALUES (:id, :ref, :name, :email)",
            dict(id=customer_id, ref=customer_ref, name=name, email=email)
        )

    def test_repo_can_retrieve_customer_by_email(self):
        _customer_id = random_customer_ref('Philip')
        _customer_ref = random_customer_ref('Philip Lunse')
        self.insert_customer(self.session, _customer_id, _customer_ref, 'Philip Lunse', 'Philip.Lunse@gmail.com')
        self.session.commit()

        _retrieved_customer = self.under_test.select_customer_by_email('Philip.Lunse@gmail.com')
        self.assertTrue(_retrieved_customer is not None)

    if __name__ == '__main__':
        unittest.main()
