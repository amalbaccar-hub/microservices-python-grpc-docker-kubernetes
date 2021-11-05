class Customer:
    def __init__(self, reference, name, email):
        self.reference = reference
        self.name = name
        self.email = email

    def __str__(self):
        return f'Customer: reference={self.reference} name= {self.name} email= {self.email}'

    def __repr__(self):
        return f'<Customer(reference={self.reference}, name={self.name}, email={self.email})>'

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference)
