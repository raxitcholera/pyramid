from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from pyramid.security import (
    Allow,
    Everyone,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Users(Base):    
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    password = Column(Text)
    group = Column(Text)

    def __init__(self, name, password,group):
        self.name = name
        self.password = password
        self.group = group

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass

Index('my_index', MyModel.name, unique=True, mysql_length=255)
