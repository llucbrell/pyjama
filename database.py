from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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

class Theme(Base):
    __tablename__ = 'themes'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    player = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    image = Column(String, nullable=True)

class Instrument(Base):
    __tablename__ = 'instruments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'), nullable=False)
    theme = relationship('Theme', back_populates='instruments')

class ParamSong(Base):
    __tablename__ = 'param_songs'
    id = Column(Integer, primary_key=True)
    param_name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    instrument = relationship('Instrument', back_populates='param_songs')

Theme.instruments = relationship('Instrument', order_by=Instrument.id, back_populates='theme')
Instrument.param_songs = relationship('ParamSong', order_by=ParamSong.id, back_populates='instrument')

engine = create_engine('sqlite:///pyjama_data.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
