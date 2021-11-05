import abc
from payment_package.domain import model


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_payment(self, payment: model.Payment):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add_payment(self, payment: model.Payment):
        self.session.add(payment)

    def list_payments(self):
        self.session.query(model.Payment).all()
