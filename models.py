from database import Base
from sqlalchemy import String, Integer, Column, Float, Table, ForeignKey, Boolean, Text, Date
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from sqlalchemy import JSON, DateTime

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)


