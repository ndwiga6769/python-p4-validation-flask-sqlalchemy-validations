import sqlalchemy

from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates


connection_string = "sqlite:///database.db"   # for SQLite, local file
db   = create_engine(connection_string)
base = declarative_base()

from sqlalchemy.orm import validates

class EmailAddress(base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email = Column(String)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("failed simple email validation")
        return address

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

email = EmailAddress(email='banana')
session.add(email)

try:
    session.commit()
except sqlalchemy.exc.IntegrityError as e:
    print("Integrity violation blocked!")
    session.rollback()