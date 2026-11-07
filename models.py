from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    bankroll = Column(Float, default=250.0)
    
    picks = relationship("Pick", back_populates="user")
    parleys = relationship("Parley", back_populates="user")

class Pick(Base):
    __tablename__ = "picks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sport = Column(String)
    match = Column(String)
    selection = Column(String)
    odds = Column(Float)
    stake = Column(Float)
    status = Column(String, default="pendiente") # pendiente, ganado, perdido, anulado
    date = Column(String)
    analysis = Column(String, nullable=True)
    confidence = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="picks")

class Parley(Base):
    __tablename__ = "parleys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    stake = Column(Float)
    status = Column(String, default="pendiente")
    date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="parleys")
    legs = relationship("ParleyLeg", back_populates="parley", cascade="all, delete-orphan")

class ParleyLeg(Base):
    __tablename__ = "parley_legs"
    id = Column(Integer, primary_key=True, index=True)
    parley_id = Column(Integer, ForeignKey("parleys.id"))
    match = Column(String)
    selection = Column(String)
    odds = Column(Float)
    status = Column(String, default="pending") # pending, won, lost

    parley = relationship("Parley", back_populates="legs")
