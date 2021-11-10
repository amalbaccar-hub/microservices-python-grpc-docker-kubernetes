# Example application code for microservices with python, grpc, docker and kubernetes
the goal of this example is mainly to learn and test grpc, docker and kubernetes. So to keep things manageable, I defined only two microservices:
1. **Customer**: is a microservice that register a new customer and performs basic CRUD operations around the customer.
2. **Payment**: is a microservice that basically execute a payment and some CRUD operations related to it.
The payment microservice interact with the customer microservice to retrieve information about the customer. 

## Requirements
* a local python 3.9 virtualenv 
* docker with docker-compose

## Building the containers
- make build
- make up
**OR**
- make all # builds and brings containers up
