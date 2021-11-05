import os

grpc_port = 50051


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 54321
    # password_file = os.environ.get("DB_PASSWORD_FILE", "abc123")
    # pf = open(password_file, 'r')
    # password = pf.read()
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "postgres", "customer"
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
