from customer_package.entrypoints.customer_service import customer_registration_pb2_grpc
from customer_package.entrypoints.customer_service.customer_registration_pb2 import *
from customer_package.adapters import orm, repository
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from customer_package import config
from customer_package.service_layer import services


class CustomerRegistration(customer_registration_pb2_grpc.CustomerRegistrationServicer):
    def __init__(self, session=None):
        orm.start_mappers()
        if not session:
            self.session = sessionmaker(bind=create_engine(config.get_postgres_uri()))()
        else:
            self.session = session

    # registration endpoint
    def register_new_customer(self, request, context):
        repo = repository.SqlAlchemyRepository(self.session)
        try:
            services.add_new_customer(request.customer.customer_ref, request.customer.name, request.customer.email,
                                      repo,
                                      self.session)

        except services.AlreadyRegisteredCustomer as e:
            return CustomerRegistrationResponse(success=False, message=f'message: {str(e)}')

        return CustomerRegistrationResponse(success=True, message=f'{str(request)} is now registered!')

    def get_customer_by_email(self, request, context):
        repo = repository.SqlAlchemyRepository(self.session)
        _customer = None
        try:
            _customer = services.get_customer_by_email(request.email, repo)

        except services.CustomerNotFoundException as e:
            return GetCustomerByEmailResponse(customer=_customer, found=False)

        return GetCustomerByEmailResponse(
            customer=Customer(customer_ref=_customer.reference, name=_customer.name, email=_customer.email), found=True)

    def get_customer_by_reference(self, request, context):
        repo = repository.SqlAlchemyRepository(self.session)
        _customer = None
        try:
            _customer = services.get_customer_by_reference(request.customer_ref, repo)

        except services.CustomerNotFoundException as e:
            return GetCustomerByReferenceResponse(customer=_customer, found=False)

        return GetCustomerByReferenceResponse(
            customer=Customer(customer_ref=_customer.reference, name=_customer.name, email=_customer.email), found=True)
