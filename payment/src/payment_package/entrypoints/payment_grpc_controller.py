from payment_package.entrypoints.payment_service import payment_pb2_grpc
from payment_package.entrypoints.payment_service.payment_pb2 import *
from payment_package.adapters import orm, repository
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from payment_package import config
from payment_package.service_layer import services
from payment_package.service_layer.stripe_lib.stripe_service import StripeService
import stripe


class PaymentController(payment_pb2_grpc.PaymentServiceServicer):
    def __init__(self, session=None):
        stripe.api_key = config.stripe_keys['secret_key']
        orm.start_mappers()
        if not session:
            self.session = sessionmaker(bind=create_engine(config.get_postgres_uri()))()
        else:
            self.session = session

    # make payment endpoint
    def pay(self, request, context) -> PaymentResponse:
        repo = repository.SqlAlchemyRepository(self.session)
        payment_service = StripeService()
        try:
            services.pay(request.payment.payment_ref, request.payment.customer_ref, request.payment.amount,
                         Currency.Name(request.payment.currency), request.payment.card_number,
                         request.payment.card_exp_month, request.payment.card_exp_year, request.payment.card_cvc, repo,
                         self.session, payment_service)
        except services.CustomerNotFoundException as e:
            return PaymentResponse(success=False, message=f'{str(e)}')
        except services.CurrencyNotSupportedException as e:
            return PaymentResponse(success=False, message=f'{str(e)}')
        except services.PaymentErrorException as e:
            return PaymentResponse(success=False, message=f'{str(e)}')

        return PaymentResponse(success=True,
                               message=f'💰 Payment received for customer ref= {request.payment.customer_ref}')
