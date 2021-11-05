# TODO replace abc (abstract class) by ducking type
import abc
from customer_package.domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_customer(self, customer: model.Customer):
        raise NotImplementedError

    @abc.abstractmethod
    def select_customer_by_email(self, email) -> model.Customer:
        raise NotImplementedError

    @abc.abstractmethod
    def select_customer_by_reference(self, customer_ref) -> model.Customer:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add_customer(self, customer: model.Customer):
        self.session.add(customer)

    def select_customer_by_email(self, email) -> model.Customer:
        return self.session.query(model.Customer).filter_by(email=email).first()

    def select_customer_by_reference(self, customer_ref) -> model.Customer:
        return self.session.query(model.Customer).filter_by(reference=customer_ref).first()

    def list_customers(self):
        return self.session.query(model.Customer).all()
