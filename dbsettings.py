from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:Netsolpk1@localhost:5432/freelance_community")
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()
def get_session():
    """
    Create a database session.
    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()