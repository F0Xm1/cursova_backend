from database import Base
from sqlalchemy import String, Integer, Column, Float, Table, ForeignKey, Boolean, Text, Date
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from sqlalchemy import JSON, DateTime

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    icon_url = Column(String, nullable=False)
    articles = relationship('Article', back_populates='category')


class Issue(Base):
    __tablename__ = 'issues'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    pdf_link = Column(String, nullable=True)
    cover_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=True)
    is_premium = Column(Boolean, default=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)

    author = relationship('Users', backref='articles')
    category = relationship('Category', back_populates='articles')
    issue = relationship('Issue', backref='articles')
    saved_by = relationship('SavedArticle', back_populates='article', cascade='all, delete-orphan')


class SavedArticle(Base):
    __tablename__ = 'saved_articles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('Users', backref='saved_articles')
    article = relationship('Article', back_populates='saved_by')


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship('Users', backref='subscriptions')


class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=True)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    results = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    article = relationship('Article', backref='polls')


class PollVote(Base):
    __tablename__ = 'poll_votes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    poll_id = Column(Integer, ForeignKey('polls.id'), nullable=False)
    selected_option = Column(String, nullable=False)
    voted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('Users', backref='poll_votes')
    poll = relationship('Poll', backref='votes')
