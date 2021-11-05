from enum import Enum


class PaymentStatus(Enum):
    ERROR = 'error'
    SUCCEEDED = 'succeeded'


class PaymentResponse:
    def __init__(self, payment_id, status: PaymentStatus, msg):
        self.payment_id = payment_id
        self.status = status.value
        self.message = msg

    def __str__(self):
        return f'PaymentStatus: id= {self.payment_id} status= {self.status.value} message= {self.message}'
