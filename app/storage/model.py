from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine

Base = declarative_base()

class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=False, nullable=False)



class Pharmacy(Base):
    __tablename__ = 'pharmacy'

    id = Column(Integer, primary_key=True)
    pharmacy_name = Column(String(240), unique=True, nullable=False)
    telephone = Column(String(15))
    address = Column(String(120))
    district_id = Column(Integer, ForeignKey('district.id'), nullable=False)
    name = relationship(District)

engine = create_engine('sqlite:///database.db')
DBSession = scoped_session(sessionmaker(bind=engine))
Base.metadata.bind = engine
Base.metadata.create_all(engine)