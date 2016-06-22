from zope.interface import implementer
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

from zope.sqlalchemy import ZopeTransactionExtension


from .meta import Base, DBSession

from pyramid_sacrud import PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW
from pyramid_sacrud.interfaces import ISacrudResource

from pyramid.security import (
    Allow,
    Everyone)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    Name = Column(Text)
    Password = Column(Text)
    Age = Column(Integer)

@implementer(ISacrudResource)
class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    Topic = Column(Text)
    ShortInfo = Column(Text)
    Data = Column(Text)
    image_name = Column(Text)
	

class Accesses(object):
    __acl__ = [ (Allow, 'group:editors', ('pyramid_sacrud_home', 'pyramid_sacrud_create', 'pyramid_sacrud_update', 'pyramid_sacrud_delete', 'pyramid_sacrud_list')),
                (Allow, 'Everyone', 'pyramid_sacrud_view') ]
    def __init__(self, request):
        pass	

#Index('my_index', MyModel.name, unique=True, mysql_length=255)
