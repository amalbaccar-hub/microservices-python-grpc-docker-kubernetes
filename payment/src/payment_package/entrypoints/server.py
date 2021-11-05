import time
from concurrent import futures

import grpc

from payment_package import config
from payment_package.entrypoints import payment_grpc_controller
from payment_package.entrypoints.payment_service import payment_pb2_grpc
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from payment_package.adapters.orm import metadata
from sqlalchemy.orm import sessionmaker


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError as e:
            print(f'postgres exception: {e} db uri {config.get_postgres_uri()}')
            time.sleep(0.5)
    raise Exception('Postgres never came up')


def run():
    engine = create_engine(config.get_postgres_uri())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        payment_grpc_controller.PaymentController(session),
        server)
    server.add_insecure_port(f'[::]:{config.payment_grpc_port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    run()
