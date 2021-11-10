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
- make up\
**OR**
- make all # builds and brings containers up

## Using secrets for docker containers
Among the best practices, it's recommended to use secrets to protect sensitive data such as database credentials.
You'll find a file named 'password.txt' under customer and payment folders, that's aimed to contain the postgres database password. Put yours there.
check 'docker-compose.yml' to see how to use secrets.\
In real world applications, such files **MUST NOT BE COMMITED** to subversion control. It's just there for demo purposes. 
