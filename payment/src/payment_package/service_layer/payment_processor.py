import abc
from payment_package.service_layer.payment_response import PaymentResponse


class AbstractPaymentProcessor(abc.ABC):

    @abc.abstractmethod
    def pay(self, amount, currency, card_number, card_exp_month, card_exp_year,
            card_cvc, payment_id=None) -> PaymentResponse:
        raise NotImplementedError
