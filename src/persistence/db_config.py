"""Module defines configuration for database connection"""
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

connection_string = os.environ['WORKSPACES_CONNECTION_STRING']
engine = create_engine(connection_string, echo=True, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
Base = declarative_base(metadata=MetaData(), bind=engine)
