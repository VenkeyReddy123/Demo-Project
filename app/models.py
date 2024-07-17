from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Corrected DATABASE_URL
DATABASE_URL = 'sqlite:///./test.db'

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

# Define the DeptTable class inheriting from Base
class DeptTable(Base):
    __tablename__ = 'DeptTable'
    deptno = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String, index=True)

# Create all tables
Base.metadata.create_all(bind=engine)
