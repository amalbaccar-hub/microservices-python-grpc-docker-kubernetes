from customer_package.domain import model
from customer_package.adapters.repository import AbstractRepository


class AlreadyRegisteredCustomer(Exception):
    pass


class CustomerNotFoundException(Exception):
    pass


def add_new_customer(reference: str, name: str, email: str, repo: AbstractRepository, session):
    # TODO check if email is valid
    _customer = repo.select_customer_by_email(email)

    if _customer:
        raise AlreadyRegisteredCustomer(f'{str(_customer)} is already registered')

    repo.add_customer(model.Customer(reference, name, email))
    session.commit()


def get_customer_by_email(email: str, repo: AbstractRepository):
    # TODO check if email is valid
    _customer = repo.select_customer_by_email(email)

    if not _customer:
        raise CustomerNotFoundException(f'customer with email {email} is not found')

    return _customer


def get_customer_by_reference(reference: str, repo: AbstractRepository):
    _customer = repo.select_customer_by_reference(reference)

    if not _customer:
        raise CustomerNotFoundException(f'customer with reference {reference} is not found')

    return _customer
