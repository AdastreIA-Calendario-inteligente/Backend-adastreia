
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ainda não sei a URL que a a lara vai usar, então deixei esse placeholder aqui
DATABASE_URL = "postgresql://user:password@localhost/adasteia_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()