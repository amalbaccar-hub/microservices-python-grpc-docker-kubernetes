import unittest
from customer.tests.unit.fake_dependencies import *
from customer_package.service_layer import services
import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_customer_ref(name=""):
    return f'customer-{name}-{random_suffix()}'


class TestServices(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeRepository()
        self.session = FakeSession()

    def tearDown(self) -> None:
        pass

    def test_register_new_customer_succeeded(self):
        _customer_ref = random_customer_ref('Justin')
        services.add_new_customer(_customer_ref, 'Justin Cruise', 'Justin.Cruise@gmail.com', self.repo,
                                  self.session)

        self.assertEqual(self.session.commited, True)
        self.assertEqual(self.repo.list_customers(), [(_customer_ref, 'Justin Cruise', 'Justin.Cruise@gmail.com')])

    def test_get_customer_by_email_succeeded(self):
        _customer = model.Customer(random_customer_ref('George Lopez'), 'George Lopez', 'George.Lopez@gmail.com')
        self.repo.add_customer(_customer)
        self.session.commit()

        retrieved_customer = services.get_customer_by_email('George.Lopez@gmail.com', self.repo)

        self.assertNotEqual(retrieved_customer, None)

    def test_get_customer_by_email_throws(self):
        _customer = model.Customer(random_customer_ref('Barbara Adolfo'), 'Barbara Adolfo', 'Barbara.Adolfo@gmail.com')

        with self.assertRaises(services.CustomerNotFoundException) as context:
            services.get_customer_by_email('Barbara.Adolfo@gmail.com', self.repo)

        self.assertTrue('customer with email Barbara.Adolfo@gmail.com is not found' in str(context.exception))

    def test_get_customer_by_reference_succeeded(self):
        _customer_ref = random_customer_ref('Jennifer Carey')
        _customer = model.Customer(_customer_ref, 'Jennifer Carey', 'Jennifer.Carey@gmail.com')
        self.repo.add_customer(_customer)
        self.session.commit()

        retrieved_customer = services.get_customer_by_reference(_customer_ref, self.repo)

        self.assertNotEqual(retrieved_customer, None)


if __name__ == '__main__':
    unittest.main()
