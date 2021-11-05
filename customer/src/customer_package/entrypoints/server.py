import time
from concurrent import futures

import grpc
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from customer_package import config
from customer_package.adapters.orm import metadata
from customer_package.entrypoints.customer_service import customer_registration_pb2_grpc
from customer_package.entrypoints import customer_registration_grpc_controller


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError as e:
            print(f'postgres exception: {e}')
            time.sleep(0.5)
    raise Exception('Postgres never came up')


def run():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_registration_pb2_grpc.add_CustomerRegistrationServicer_to_server(
        customer_registration_grpc_controller.CustomerRegistration(session),
        server)
    server.add_insecure_port(f'[::]:{config.grpc_port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    run()
