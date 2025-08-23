from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os

DATABASE = {
    "drivername": os.getenv("MYSQL_DRIVERNAME", "mysql+pymysql"),
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": os.getenv("MYSQL_PORT", "3307"),
    "user": os.getenv("MYSQL_USER", "user"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "name": os.getenv("MYSQL_DATABASE", "db_name"),
}

DATABASE_URL = (
    f"{DATABASE['drivername']}://{DATABASE['user']}:{DATABASE['password']}@"
    f"{DATABASE['host']}:{DATABASE['port']}/{DATABASE['name']}"
)

DELETE_MODE = os.getenv("DELETE_MODE", "soft")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
