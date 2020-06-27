from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.persistence.db_config import Base

class WorkspaceEntity(Base):
    __tablename__ = 'workspaces'
    
    id = Column(Integer, primary_key=True)
    workspace_type = Column(String(255))
    workspace_name = Column(String(255))
    workspace_id = Column(String(255))
    generated_channel_id = Column(String(255))
    generated_channel_name = Column(String(255))
    auth_token = Column(String(255), nullable=True)
    created_on = Column(DateTime(), default=datetime.utcnow())
    updated_on = Column(DateTime(), default=datetime.utcnow(), onupdate=datetime.utcnow())
