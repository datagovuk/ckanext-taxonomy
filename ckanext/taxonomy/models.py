import uuid
import json

from sqlalchemy import Table, Column, MetaData, ForeignKey
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
    name = Column(types.UnicodeText)
    label = Column(types.UnicodeText)
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

    labels = Column(types.UnicodeText)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_label(self, language):
        """
        Get the label for this.
        """
        labels = self.get_labels()
        result = (l for l in labels if l['language'] == language)
        if any(result):
            return result[0]
        # Default to English label
        return self.label

    def get_labels(self):
        try:
            lbls = json.loads(self.labels)
        except:
            return []
        return lbls

    def set_labels(self, label_list):
        """
        Expected that label_list is a list of dicts that looks like
        { "label": "", "language": "fr" }
        """
        labels = label_list or []
        try:
            self.labels = json.dumps(label_list)
        except:
            pass

    @classmethod
    def get(cls, name_or_id):
        q = model.Session.query(TaxonomyTerm)\
            .filter(TaxonomyTerm.name == name_or_id)
        obj = q.first()
        if not obj:
            q = model.Session.query(TaxonomyTerm)\
                .filter(TaxonomyTerm.id == name_or_id)
            obj = q.first()
        return obj

    @classmethod
    def by_uri(cls, uri):
        q = model.Session.query(TaxonomyTerm)\
            .filter(TaxonomyTerm.uri == uri)
        return q.first()

    def as_dict(self, language="en"):
        d = {
            'id': self.id,
            'name': self.name,
            'label': self.get_label(language),
            'uri': self.uri,
            'labels': self.get_labels(),
            'taxonomy_id': self.taxonomy_id,
            'parent_id': self.parent_id
        }
        return d

    def __repr__(self):
        return u"<Taxonomy Term: %s>" % (self.name)


def init_tables():
    Base.metadata.create_all(model.meta.engine)


def remove_tables():
    TaxonomyTerm.__table__.drop(model.meta.engine, checkfirst=False)
    Taxonomy.__table__.drop(model.meta.engine, checkfirst=False)
