from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    module = Column(String, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    collector_id = Column(String, nullable=False)
    schema_json = Column(Text, nullable=True)
    health = Column(String, default="unknown")
    last_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Snapshot(Base):
    __tablename__ = "snapshots"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False)
    raw_json = Column(JSON, nullable=False)
    hash = Column(String, nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ok")

class Change(Base):
    __tablename__ = "changes"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False)
    change_type = Column(String, nullable=False)
    before = Column(JSON, nullable=True)
    after = Column(JSON, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)

class HealEvent(Base):
    __tablename__ = "heal_events"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    success = Column(String, nullable=False)
    response_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
