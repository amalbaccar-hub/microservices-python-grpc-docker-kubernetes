from payment_package.service_layer.payment_processor import AbstractPaymentProcessor
import stripe
from payment_package.service_layer.payment_response import PaymentStatus, PaymentResponse


def generate_response(intent) -> PaymentResponse:
    status = intent.status
    if status == 'requires_action' or status == 'requires_source_action':
        return PaymentResponse(payment_id=intent.id, status=PaymentStatus.ERROR, msg=f'card requires authentication.'
                                                                                     f' payment id= {intent.id}')
    elif status == 'requires_payment_method' or status == 'requires_source':
        return PaymentResponse(payment_id=intent.id, status=PaymentStatus.ERROR,
                               msg='Your card was denied, please provide a new payment method')
    elif status == 'succeeded':
        return PaymentResponse(payment_id=intent.id, status=PaymentStatus.SUCCEEDED, msg='💰 Payment received!')


class StripeService(AbstractPaymentProcessor):

    def pay(self, amount, currency, card_number, card_exp_month, card_exp_year,
            card_cvc, payment_id=None) -> PaymentResponse:
        # I used synchronous payment
        # means one time payment made payment_server side
        # this is not best practice
        # check official stripe docu
        try:
            if not payment_id:
                payment_method_data = {'type': 'card',
                                       'card': {
                                           'number': card_number,
                                           'exp_month': card_exp_month,
                                           'exp_year': card_exp_year,
                                           'cvc': card_cvc
                                       }
                                       }
                method = stripe.PaymentMethod.create(**payment_method_data)

                payment_intent_data = {'payment_method': method.id,
                                       'amount': amount,
                                       'currency': str(currency),  # stripe accepts lowercase currencies
                                       'confirmation_method': 'manual',
                                       'confirm': 'true'
                                       }

                intent = stripe.PaymentIntent.create(**payment_intent_data)
            else:
                # confirm the PaymentIntent to collect the money
                intent = stripe.PaymentIntent.confirm(payment_id)

            return generate_response(intent)

        except stripe.error.StripeError as e:
            print(str(e))
            return PaymentResponse(payment_id=None, status=PaymentStatus.ERROR, msg=str(e))
        except Exception as e:
            print(str(e))
            return PaymentResponse(payment_id=None, status=PaymentStatus.ERROR, msg=str(e))
