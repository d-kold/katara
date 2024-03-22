from sqlalchemy import create_engine, Column, Integer, DateTime, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:////app/data/events.db"  # Your SQLite database file
# DATABASE_URL = "sqlite:////home/kdcore/PycharmProjects/katara/data/events.db"  # Your SQLite database file

Base = declarative_base()


class SwitchEvent(Base):
    __tablename__ = "switch_events"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)  # 'on' or 'off'
    timestamp = Column(DateTime, default=datetime.utcnow)


# Engine and session setup
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
