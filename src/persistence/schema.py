from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from workspace_entity import WorkspaceEntity
from db_config import Base

class Schema:
    def __init__(self):
        pass
        # connecting_string = os.environ['WORKSPACES_CONNECTION_STRING']
        # self.engine = create_engine(connecting_string, echo=True)
        # self.engine.execute('CREATE DATABASE pub_workspaces')
        # self.metadata = MetaData()

    def create(self):
        Base.metadata.create_all()
        return

    def update(self):
        # TODO: How do we handle migrations on existing production db? view sqlalchemy logs
        Base.metadata.create_all()
        return    

    def drop(self):
        Base.metadata.drop_all()
        return

    def seed(self):
        pass

    def create_if_not_exist(self):
        pass

schema = Schema()
schema.drop()
