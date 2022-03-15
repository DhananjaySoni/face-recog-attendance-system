import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# setup db code
Base = declarative_base()

# create table as python class
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True)
    
    name=Column(String)
    roll_no=Column(String,unique=True)
    section=Column(String)
    created_on = Column(DateTime,default=datetime.now)
    path = Column(String)

    def __str__(self):
        return f'{self.name}->{self.roll_no}'
    
    def __repr__(self) -> str:
        return f'{self.name}-{self.roll_no}'

class Attendance(Base):
    __tablename__='attendance'
    id = Column(Integer,primary_key=True) 
    student=Column(Integer,ForeignKey(Student.id))
    taken_on = Column(DateTime,default=datetime.now)
    

    def __str__(self):
        return f'{self.student}->{self.taken_on}'
    
    def __repr__(self) -> str:
        return f'{self.student}-{self.taken_on}'  


# create database
if __name__ == "__main__":
    engine = create_engine("sqlite:///db.sqlite3")
    Base.metadata.create_all(engine)