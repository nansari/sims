# https://github.com/dr5hn/countries-states-cities-database
# https://flask-sqlalchemy.readthedocs.io/en/stable/
# http://medium.com/@ramanbazhanau/mastering-sqlalchemy-a-comprehensive-guide-for-python-developers-ddb3d9f2e829

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from flask_login import UserMixin
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    """Load user."""
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    """User model."""
    # UserMixin provides - is_authenticated, is_active, is_anonymous, get_id()
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,)
                                            
    password: so.Mapped['Password'] = so.relationship(back_populates='user', cascade='all, delete-orphan')
    bithdate: so.Mapped[int] = so.mapped_column(
        sa.Integer(),
        sa.CheckConstraint('bithdate BETWEEN 1950 and 2099'))
    
    
    @property
    def password_hash(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        """Set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password."""
        if self.password:
            return check_password_hash(self.password.password_hash, password)
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Password(db.Model):
    """Password model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), unique=True)
    user: so.Mapped['User'] = so.relationship(back_populates='password')
    
# class Post(db.Model):
#     """Post model."""
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     body: so.Mapped[str] = so.mapped_column(sa.String(140))
#     timestamp: so.Mapped[datetime] = so.mapped_column(
#         index=True, default=lambda: datetime.now(timezone.utc))
#     user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
#                                                index=True)

#     author: so.Mapped[User] = so.relationship(back_populates='posts')

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

class Role(db.Model):
    """Role model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(32), unique=True)

class UserRole(db.Model):
    """User role model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Role.id))