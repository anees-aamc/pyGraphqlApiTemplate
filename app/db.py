from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load database URL from env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/pyApiTest")

# Create synchronous engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
