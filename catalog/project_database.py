from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base=declarative_base()

class DummyPassword(Base, UserMixin):
	__tablename__='password_data'
	todayDate = datetime.today().strftime('%Y-%m-%d') # YYYY-MM-DD

	id =Column(Integer,primary_key=True)
	email=Column(String(150),nullable=False)
	password=Column(String(100),nullable=False)	
	status=Column(Integer,default=0)
	todaydate = Column(String(100), default=todayDate)



engine=create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
print("Database Created")
