from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy_serializer import SerializerMixin

product_database = create_engine("postgresql://qyzfldnbruuurp:b302ab9d2122480b5b670330469dcb4e585671e89778216e3f6f2ff033b32d26@ec2-3-219-52-220.compute-1.amazonaws.com:5432/d60shomks5uoek")
base = declarative_base(product_database)
Session = sessionmaker(bind = product_database)
session = Session()


class ProductData(base,SerializerMixin):
    __tablename__ = 'ProductDataInfo'
    id = Column(Integer,primary_key = True)
    product_description = Column(String,nullable = False)
    product_hs_code = Column(String,nullable = False)
    product_value_unit = Column(String,nullable = False)
    date_created = Column(DateTime(),default = datetime.utcnow())

class UserDataInfo(base):
    __tablename__ = 'UserDetails'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(20),nullable = False)
    last_name = Column(String(20),nullable = False)
    user_email = Column(String,nullable = False)
    user_password = Column(String,nullable = False)
    entry_date = Column(DateTime, default = datetime.utcnow())

# base.metadata.create_all(product_database)
