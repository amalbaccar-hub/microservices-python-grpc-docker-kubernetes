import logging

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String
)
from sqlalchemy.orm import mapper

from payment_package.domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

payments = Table(
    "payments",
    metadata,
    Column("id", String(255), primary_key=True),
    Column("reference", String(255)),
    Column("customer_ref", String(255)),
    Column("amount", Integer),
    Column("currency", String(50)),
    Column("card_number", String(255)),
    Column("card_exp_month", Integer),
    Column("card_exp_year", Integer),
    Column("card_cvc", String(15))
)


def start_mappers():
    logger.info("starting mappers")
    mapper(model.Payment, payments)
    # mapper(model.Customer, _customers, properties={"_payments": relationship(model.Payment, primaryjoin=
    # (_customers.c.id == payments.c.customer_id), collection_class=set)}, )
