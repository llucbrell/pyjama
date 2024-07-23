from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Configuration(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    port = Column(String, nullable=False)
    active = Column(Boolean, default=False)

class Sampler(Base):
    __tablename__ = 'samplers'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    filename = Column(String, nullable=False)

engine = create_engine('sqlite:///pyjama_data.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
