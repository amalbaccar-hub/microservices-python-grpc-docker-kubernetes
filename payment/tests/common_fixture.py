import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_customer_ref(name=""):
    return f'customer-{name}-{random_suffix()}'


def random_payment_ref(name=''):
    return f'payment-{name}-{random_suffix()}'
