import logging

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String
)
from sqlalchemy.orm import mapper

from customer_package.domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

customers = Table(
    "_customers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("name", String(255)),
    Column("email", String(255)),
)


def start_mappers():
    logger.info("starting mappers")
    mapper(model.Customer, customers)
