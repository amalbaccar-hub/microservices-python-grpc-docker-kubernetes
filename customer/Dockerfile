FROM python:3.9-slim-buster

RUN python -m pip install --upgrade pip
COPY customer/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt

RUN mkdir -p /service
COPY customer/src/ /service/src/
COPY protobuf/ /service/protobuf/
RUN pip install -e /service/src

WORKDIR /service/src/customer_package/entrypoints

RUN python -m grpc_tools.protoc -I ../../../protobuf --python_out=. \
           --grpc_python_out=. ../../../protobuf/customer_service/customer_registration.proto

EXPOSE 50051
ENTRYPOINT ["python","server.py"]
