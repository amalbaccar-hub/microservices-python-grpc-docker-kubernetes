import os

stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

customer_grpc_port = 50051
payment_grpc_port = 50053


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 54322
    # password_file = os.environ.get("DB_PASSWORD_FILE", "abc123")
    # pf = open(password_file, 'r')
    # password = pf.read()
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "postgres", "payment"
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
