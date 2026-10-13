from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True)
    hours = Column(Integer)
    form = Column(String(50))

    applications = relationship("Application", back_populates="program")


class Listener(Base):
    __tablename__ = "listeners"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    phone = Column(String(20))
    snils = Column(String(20), unique=True)
    organization = Column(String(255))

    applications = relationship("Application", back_populates="listener")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    listener_id = Column(Integer, ForeignKey("listeners.id"))
    program_id = Column(Integer, ForeignKey("programs.id"))
    status = Column(String(50), default="new")
    created_at = Column(Date)
    comment = Column(Text)

    listener = relationship("Listener", back_populates="applications")
    program = relationship("Program", back_populates="applications")