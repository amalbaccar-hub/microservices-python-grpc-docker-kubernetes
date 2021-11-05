import grpc
from customer_package.entrypoints.customer_service.customer_registration_pb2_grpc import CustomerRegistrationStub
from customer_package.entrypoints.customer_service.customer_registration_pb2 import *
import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_customer_id(name: str = ""):
    return f'customer-{name}-{random_suffix()}'


def run():
    channel = grpc.insecure_channel("localhost:50051")
    client = CustomerRegistrationStub(channel)

    response = client.register_new_customer(CustomerRegistrationRequest(
        customer=Customer(customer_ref=random_customer_id('Stephanie Gansh'), name='Stephanie Gansh',
                          email='Stephanie.Gansh@gmail.com')))

    print(f'response flag {response.success}')
    print(f'response message {response.message}')


def exec_get_by_ref():
    channel = grpc.insecure_channel("localhost:50051")
    client = CustomerRegistrationStub(channel)

    response = client.get_customer_by_reference(GetCustomerByReferenceRequest(
        customer_ref='customer-Stephanie Gansh-c07c30'))

    print(f'is customer found: {response.found}')
    if response.found:
        print(f'customer: {response.customer.customer_ref}, {response.customer.name}, {response.customer.email}')


if __name__ == '__main__':
    run()
    exec_get_by_ref()
