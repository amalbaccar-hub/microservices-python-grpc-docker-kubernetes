from customer_package.adapters.repository import AbstractRepository
from customer_package.domain import model


class FakeRepository(AbstractRepository):
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

    def list_customers(self):
        return list(self._customers)


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True
