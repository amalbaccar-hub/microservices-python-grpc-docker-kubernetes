class Payment:
    def __init__(self, payment_id, payment_ref, customer_ref, amount, currency, card_number, card_exp_month,
                 card_exp_year,
                 card_cvc):
        self.id = payment_id
        self.reference = payment_ref
        self.customer_ref = customer_ref
        self.amount = amount
        self.currency = currency
        self.card_number = card_number
        self.card_exp_month = card_exp_month
        self.card_exp_year = card_exp_year
        self.card_cvc = card_cvc

    def __str__(self):
        return f'Payment: payment_ref= {self.reference} customer_ref= {self.customer_ref} amount= {self.amount} ' \
               f'currency= {self.currency} card_number= {self.card_number} card_exp_month= {self.card_exp_month} ' \
               f'card_exp_year= {self.card_exp_year} card_cvc= {self.card_cvc}'

    def __repr__(self):
        return f'<Payment(payment_ref={self.reference}, customer_ref={self.customer_ref}, amount={self.amount}, ' \
               f'currency={self.currency}, card_number={self.card_number}, card_exp_month={self.card_exp_month}, ' \
               f'card_exp_year={self.card_exp_year}, card_cvc={self.card_cvc})>'

    def __eq__(self, other):
        if not isinstance(other, Payment):
            return False
        return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference)
