from sqlalchemy import create_engine, Column, Numeric, String, \
    text, DateTime, Integer, Text, ForeignKey, Boolean, Index
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import settings


Base = declarative_base()
metadata = Base.metadata


def db_connect():
    """
    Creates a SQLAlchemy engine with the database URL defined by
    the DATABASE variable in settings.py

    Returns: sqlalchemy.engine.Engine object
    """
    return create_engine(URL(**settings.DATABASE))


class BubbleTea(Base):
    """
    SQLAlchemy model used to represent the bubble_tea table
    """
    __tablename__ = 'bubble_tea'

    id = Column(String(32), primary_key=True)
    alias = Column(String(255))
    name = Column(String(128), index=True)
    country = Column(String(128), index=True)
    address1 = Column(String(128))
    address2 = Column(String(128),
                      server_default=text("NULL::character varying"))
    address3 = Column(String(128),
                      server_default=text("NULL::character varying"))
    city = Column(String(128))
    state = Column(String(128), server_default=text("NULL::character varying"))
    zip_code = Column(String(128),
                      server_default=text("NULL::character varying"))
    phone = Column(String(32))
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    rating = Column(Numeric(2, 1))
    review_count = Column(Integer)
    url = Column(Text)
    insert_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class ZipCode(Base):
    """
    SQLAlchemy model used to represent the zip_code table
    """
    __tablename__ = 'zip_code'

    id = Column(Integer, primary_key=True, autoincrement=True)
    zip = Column(String(10))
    type = Column(String(255))
    decomissioned = Column(String(20))
    primary_city = Column(String(255))
    acceptable_cities = Column(Text)
    unacceptable_cities = Column(Text)
    state = Column(String(255))
    county = Column(String(255))
    timezone = Column(String(255))
    area_code = Column(String(255))
    world_region = Column(String(255))
    country = Column(String(255))
    latitude = Column(String(255))
    longitude = Column(String(255))
    irs_estimated_population = Column(String(255))
    insert_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Hours(Base):
    """
    SQLAlchemy model used to represent the hours table
    """
    __tablename__ = 'hours'
    __table_args__ = (
        Index('idx_bubble_tea_id_day', 'bubble_tea_id', 'day', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    bubble_tea_id = Column(ForeignKey('bubble_tea.id'))
    day = Column(Integer)
    start = Column(String(4))
    end = Column(String(4))
    is_overnight = Column(Boolean)
    insert_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    bubble_tea = relationship('BubbleTea')
