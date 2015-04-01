import uuid
import json

from sqlalchemy import Table, Column, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy import types, orm
from sqlalchemy.sql import select
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

import ckan.model as model
from ckan.lib.base import *


log = __import__('logging').getLogger(__name__)

Base = declarative_base()
metadata = MetaData()


def make_uuid():
    return unicode(uuid.uuid4())


class Taxonomy(Base):
    """
    Contains the detail about a specific taxonomy which will contain a
    hierarchy of TaxonomyTerms
    """
    __tablename__ = 'taxonomy'
    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    name = Column(types.UnicodeText, unique=True)
    title = Column(types.UnicodeText)
    uri = Column(types.UnicodeText)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get(cls, name_or_id):
        q = model.Session.query(Taxonomy).filter(Taxonomy.name == name_or_id)
        obj = q.first()
        if not obj:
            q = model.Session.query(Taxonomy).filter(Taxonomy.id == name_or_id)
            obj = q.first()
        return obj

    @classmethod
    def by_uri(cls, uri):
        return model.Session.query(Taxonomy)\
            .filter(Taxonomy.uri == uri).first()

    def as_dict(self, with_terms=False):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'uri': self.uri
        }

    def __repr__(self):
        return u"<Taxonomy: %s>" % (self.name)


class TaxonomyTerm(Base):
    """
    """
    __tablename__ = 'taxonomy_term'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    label = Column(types.UnicodeText)
    description = Column(types.UnicodeText)
    uri = Column(types.UnicodeText)

    taxonomy_id = Column(types.UnicodeText, ForeignKey('taxonomy.id'),
                         nullable=False)

    parent_id = Column(types.UnicodeText, ForeignKey('taxonomy_term.id'))
    parent = relationship(
        'TaxonomyTerm',
        primaryjoin="TaxonomyTerm.id==TaxonomyTerm.parent_id",
        backref='children', remote_side='TaxonomyTerm.id')

    taxonomy = relationship(
        Taxonomy,
        primaryjoin="TaxonomyTerm.taxonomy_id==Taxonomy.id",
        backref='terms')


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def get(cls, uri_or_id):
        q = model.Session.query(TaxonomyTerm)\
            .filter(TaxonomyTerm.uri == uri_or_id)
        obj = q.first()
        if not obj:
            q = model.Session.query(TaxonomyTerm)\
                .filter(TaxonomyTerm.id == uri_or_id)
            obj = q.first()
        return obj

    @classmethod
    def by_uri(cls, uri):
        q = model.Session.query(TaxonomyTerm)\
            .filter(TaxonomyTerm.uri == uri)
        return q.first()

    def as_dict(self):
        d = {
            'id': self.id,
            'label': self.label,
            'description': self.description,
            'uri': self.uri,
            'taxonomy_id': self.taxonomy_id,
            'parent_id': self.parent_id
        }
        return d

    def __repr__(self):
        return u"<Taxonomy Term: %s>" % (self.label)

class TaxonomyTermExtra(Base):
    """
    """
    __tablename__ = 'taxonomy_term_extra'
    __table_args__ = (UniqueConstraint('term_id', 'label'),)
    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    label = Column(types.UnicodeText)
    value = Column(types.UnicodeText)

    term_id = Column(types.UnicodeText, ForeignKey('taxonomy_term.id'), nullable=False)
    term = relationship(
        'TaxonomyTerm',
        primaryjoin="TaxonomyTerm.id==TaxonomyTermExtra.term_id",
        backref='metadata')


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_dict(self):
        d = {
            'id': self.id,
            'label': self.label,
            'value': self.value,
        }
        return d

    @classmethod
    def get(cls, name_or_id):
        q = model.Session.query(TaxonomyTermExtra).filter(TaxonomyTermExtra.id == name_or_id)
        obj = q.first()
        return obj

    @classmethod
    def by_term_and_label(cls, term_id, label):
        q = model.Session.query(TaxonomyTermExtra)\
                        .filter(TaxonomyTermExtra.term_id == term_id)\
                        .filter(TaxonomyTermExtra.label == label)
        obj = q.first()
        return obj

def init_tables():
    Base.metadata.create_all(model.meta.engine)


def remove_tables():
    TaxonomyTermExtra.__table__.drop(model.meta.engine, checkfirst=False)
    TaxonomyTerm.__table__.drop(model.meta.engine, checkfirst=False)
    Taxonomy.__table__.drop(model.meta.engine, checkfirst=False)
