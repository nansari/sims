"""
This module defines the database models for the Flask application.

It includes models for users, passwords, classes, batches, regions, groups,
and other application-specific data structures. The models are defined using
SQLAlchemy and include relationships between different tables. It also
includes a base model with common fields for tracking creation and update
timestamps and users.
"""
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
from sqlalchemy_utils import EmailType
from sqlalchemy import BigInteger

# Import all models to ensure they are registered with SQLAlchemy



@login.user_loader
def load_user(user_id):
    """Load user."""
    return db.session.get(User, int(user_id))

class BaseModel(db.Model):
    """Base model for other models to inherit from."""
    __abstract__ = True
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    """User model."""
    # UserMixin provides - is_authenticated, is_active, is_anonymous, get_id()
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,)
    gender: so.Mapped[str] = so.mapped_column(sa.String(1), nullable=False)

    password: so.Mapped['Password'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['Password.user_id'])
    contact: so.Mapped['Contact'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['Contact.user_id'])
    home_address: so.Mapped['HomeAddress'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['HomeAddress.user_id'])
    resident_address: so.Mapped['ResidentAddress'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['ResidentAddress.user_id'])
    other_details: so.Mapped['OtherDetail'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['OtherDetail.user_id'])
    progress_record: so.Mapped[list['ProgressRecord']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['ProgressRecord.user_id'])
    attendance: so.Mapped[list['UserAttendance']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['UserAttendance.user_id'])
    user_temperament: so.Mapped[list['UserTemperament']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['UserTemperament.user_id'])
    user_registration_status: so.Mapped[list['UserRegStatus']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['UserRegStatus.user_id'])
    callout_time: so.Mapped['CallOutTime'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['CallOutTime.user_id'])
    photo: so.Mapped['Photo'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['Photo.user_id'])
    test_session_score: so.Mapped[list['TestSessionScore']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['TestSessionScore.user_id'])
    user_task: so.Mapped[list['UserTask']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['UserTask.user_id'])
    user_skill: so.Mapped[list['UserSkill']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['UserSkill.user_id'])
    user_dua: so.Mapped[list['UserDua']] = so.relationship(back_populates='user', cascade='all, delete-orphan', foreign_keys=['UserDua.user_id'])
    aamal: so.Mapped['Aaamal'] = so.relationship(back_populates='user', cascade='all, delete-orphan', uselist=False, foreign_keys=['Aaamal.user_id'])
    gender: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=True)
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

class Contact(BaseModel):
    """Contact model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, nullable=False)
    mobile: so.Mapped[int] = so.mapped_column(sa.BigInteger, nullable=True)
    whatsapp: so.Mapped[int] = so.mapped_column(sa.BigInteger, nullable=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256), unique=True, nullable=False)

    user: so.Mapped['User'] = so.relationship(back_populates='contact', foreign_keys=[user_id])
    password: so.Mapped['Password'] = so.relationship(back_populates='contact', uselist=False, foreign_keys='Password.email')

    def __repr__(self):
        return '<Contact {}>'.format(self.email)

class Password(db.Model):
    """Password model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    attempt_counts: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    is_allowed: so.Mapped[int] = so.mapped_column(sa.Integer, default=False)
    force_change: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    last_attempt_time: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    last_successful_attempt_time: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(256), sa.ForeignKey('contact.email'), unique=True, nullable=False)
    user: so.Mapped['User'] = so.relationship(back_populates='password')
    contact: so.Mapped['Contact'] = so.relationship(back_populates='password', foreign_keys=[email])



class HomeAddress(BaseModel):
    """HomeAddress model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, nullable=False)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'), nullable=False)
    state_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('states.id'), nullable=False)
    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('cities.id'), nullable=False)
    area: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)
    zip: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='home_address', foreign_keys=[user_id])
    country: so.Mapped['Countries'] = so.relationship(foreign_keys=[country_id])
    state: so.Mapped['States'] = so.relationship(foreign_keys=[state_id])
    city: so.Mapped['Cities'] = so.relationship(foreign_keys=[city_id])

    def __repr__(self):
        return '<HomeAddress UserID: {}>'.format(self.user_id)

class ResidentAddress(BaseModel):
    """ResidentAddress model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, nullable=False)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'), nullable=False)
    state_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('states.id'), nullable=False)
    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('cities.id'), nullable=False)
    area: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)
    zip: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='resident_address', foreign_keys=[user_id])
    country: so.Mapped['Countries'] = so.relationship(foreign_keys=[country_id])
    state: so.Mapped['States'] = so.relationship(foreign_keys=[state_id])
    city: so.Mapped['Cities'] = so.relationship(foreign_keys=[city_id])

    def __repr__(self):
        return '<ResidentAddress UserID: {}>'.format(self.user_id)

class OtherDetail(BaseModel):
    """OtherDetail model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, nullable=False)
    education: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=False)
    profession: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=False)
    visa_status: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)
    citizenship: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)
    spouse: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    son: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    daughter: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='other_details', foreign_keys=[user_id])

    def __repr__(self):
        return '<OtherDetail UserID: {}>'.format(self.user_id)

class ProgressRecord(BaseModel):
    """ProgressRecord model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    note: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='progress_record', foreign_keys=[user_id])

    def __repr__(self):
        return '<ProgressRecord UserID: {}>'.format(self.user_id)

class AttendanceStatusLookup(db.Model):
    """AttendanceStatusLookup model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(1), unique=True, nullable=False)

    def __repr__(self):
        return '<AttendanceStatusLookup {}>'.format(self.status)

class ClassSession(BaseModel):
    """ClassSession model."""
    __table_args__ = (sa.UniqueConstraint('class_date', 'class_batch_id'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_date: so.Mapped[datetime] = so.mapped_column(sa.Date, nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    teacher_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)

    class_batch: so.Mapped['ClassBatch'] = so.relationship()
    teacher: so.Mapped['User'] = so.relationship(foreign_keys=[teacher_id])

    def __repr__(self):
        return f'<ClassSession Date: {self.class_date} Batch: {self.class_batch_id}>'

class UserAttendance(BaseModel):
    """UserAttendance model."""
    __table_args__ = (sa.UniqueConstraint('user_id', 'class_session_id'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_session.id'), nullable=False)
    attendance_status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('attendance_status_lookup.id'), nullable=False)
    note: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    late_by_min: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    left_early_by_min: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='attendance', foreign_keys=[user_id])
    class_session: so.Mapped['ClassSession'] = so.relationship()
    attendance_status: so.Mapped['AttendanceStatusLookup'] = so.relationship()

    def __repr__(self):
        return f'<UserAttendance UserID: {self.user_id} SessionID: {self.class_session_id}>'

class TemperamentLookup(db.Model):
    """TemperamentLookup model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    temperament: so.Mapped[str] = so.mapped_column(sa.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<TemperamentLookup {}>'.format(self.temperament)

class UserTemperament(BaseModel):
    """UserTemperament model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    temperament_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('temperament_lookup.id'), nullable=False)
    note: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='user_temperament', foreign_keys=[user_id])
    temperament: so.Mapped['TemperamentLookup'] = so.relationship()

    def __repr__(self):
        return f'<UserTemperament UserID: {self.user_id} TemperamentID: {self.temperament_id}>'

class RegStatusLookup(db.Model):
    """RegStatusLookup model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)

    def __repr__(self):
        return '<RegStatusLookup {}>'.format(self.status)

class UserRegStatus(BaseModel):
    """UserRegStatus model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('reg_status_lookup.id'), nullable=False)

    user: so.Mapped['User'] = so.relationship(back_populates='user_registration_status', foreign_keys=[user_id])
    status: so.Mapped['RegStatusLookup'] = so.relationship()

    def __repr__(self):
        return f'<UserRegStatus UserID: {self.user_id} StatusID: {self.status_id}>'

class CallOutTime(BaseModel):
    """CallOutTime model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    hours: so.Mapped[datetime] = so.mapped_column(sa.Time, nullable=False)
    timezone: so.Mapped[str] = so.mapped_column(sa.String(16), nullable=False)

    user: so.Mapped['User'] = so.relationship(back_populates='callout_time', foreign_keys=[user_id])

    def __repr__(self):
        return f'<CallOutTime UserID: {self.user_id} Hours: {self.hours}>'

class Photo(BaseModel):
    """Photo model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, nullable=False)
    picture: so.Mapped[bytes] = so.mapped_column(sa.LargeBinary, nullable=False)

    user: so.Mapped['User'] = so.relationship(back_populates='photo', foreign_keys=[user_id])

    def __repr__(self):
        return '<Photo UserID: {}>'.format(self.user_id)

class TestSession(BaseModel):
    """TestSession model."""
    __table_args__ = (sa.UniqueConstraint('test_date', 'class_batch_id'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    test_date: so.Mapped[datetime] = so.mapped_column(sa.Date, nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    max_score: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    class_batch: so.Mapped['ClassBatch'] = so.relationship()

    def __repr__(self):
        return f'<TestSession Date: {self.test_date} Batch: {self.class_batch_id}>'

class TestSessionScore(BaseModel):
    """TestSessionScore model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    test_session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('test_session.id'), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    score: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    note: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    test_session: so.Mapped['TestSession'] = so.relationship()
    user: so.Mapped['User'] = so.relationship(back_populates='test_session_score', foreign_keys=[user_id])

    def __repr__(self):
        return f'<TestSessionScore UserID: {self.user_id} TestSessionID: {self.test_session_id}>'

class Task(BaseModel):
    """Task model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    due_date: so.Mapped[datetime] = so.mapped_column(sa.Date, nullable=False)

    class_batch: so.Mapped['ClassBatch'] = so.relationship()

    def __repr__(self):
        return '<Task Name: {}>'.format(self.name)

class UserTask(BaseModel):
    """UserTask model."""
    __table_args__ = (sa.UniqueConstraint('user_id', 'task_id'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    task_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('task.id'), nullable=False)
    status: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False)
    note: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='user_task', foreign_keys=[user_id])
    task: so.Mapped['Task'] = so.relationship()

    def __repr__(self):
        return f'<UserTask UserID: {self.user_id} TaskID: {self.task_id}>'

class SkillLookup(db.Model):
    """SkillLookup model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    skill: so.Mapped[str] = so.mapped_column(sa.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<SkillLookup {}>'.format(self.skill)

class UserSkill(BaseModel):
    """UserSkill model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    skill_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('skill_lookup.id'), nullable=False)
    skill_detail: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='user_skill', foreign_keys=[user_id])
    skill: so.Mapped['SkillLookup'] = so.relationship()

    def __repr__(self):
        return f'<UserSkill UserID: {self.user_id} SkillID: {self.skill_id}>'

class DuaCatLookup(db.Model):
    """DuaCatLookup model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    dua: so.Mapped[str] = so.mapped_column(sa.String(32), unique=True, nullable=False)

    def __repr__(self):
        return '<DuaCatLookup {}>'.format(self.dua)

class UserDua(BaseModel):
    """UserDua model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    dua_cat_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('dua_cat_lookup.id'), nullable=False)
    class_session_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_session.id'), nullable=False)
    dua_detail: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='user_dua', foreign_keys=[user_id])
    dua_category: so.Mapped['DuaCatLookup'] = so.relationship()
    class_session: so.Mapped['ClassSession'] = so.relationship()

    def __repr__(self):
        return f'<UserDua UserID: {self.user_id} DuaCatID: {self.dua_cat_id}>'

class Aaamal(BaseModel):
    """Aaamal model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    fazar_ba_jamat: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    roza: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    zikr: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    tahajjud: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    sadka: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    user: so.Mapped['User'] = so.relationship(back_populates='aamal')

    def __repr__(self):
        return '<Aaamal UserID: {}>'.format(self.user_id)

class ClassName(BaseModel):
    """ClassName model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(8), unique=True, nullable=False)

    def __repr__(self):
        return '<ClassName {}>'.format(self.name)

class ClassBatchStatus(db.Model):
    """ClassBatchStatus lookup table."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)

class ClassBatch(BaseModel):
    """ClassBatch model."""
    __table_args__ = (sa.UniqueConstraint('class_name_id', 'batch_no'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_name_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_name.id'), nullable=False)
    batch_no: so.Mapped[str] = so.mapped_column(sa.String(3), nullable=False)
    start_date: so.Mapped[datetime] = so.mapped_column(nullable=False)
    status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch_status.id'), nullable=False)

    class_name: so.Mapped['ClassName'] = so.relationship()
    status: so.Mapped['ClassBatchStatus'] = so.relationship()

class ClassRegion(BaseModel):
    """ClassRegion model."""
    __table_args__ = (sa.UniqueConstraint('class_name_id', 'class_batch_id', 'section'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_name_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_name.id'), nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    section: so.Mapped[str] = so.mapped_column(sa.String(1), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    class_name: so.Mapped['ClassName'] = so.relationship()
    class_batch: so.Mapped['ClassBatch'] = so.relationship()

class ClassGroup(BaseModel):
    """ClassGroup model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    class_region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_region.id'), nullable=False, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    start_index: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    end_index: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    class_region: so.Mapped['ClassRegion'] = so.relationship()

class ClassGroupMentor(BaseModel):
    """ClassGroupMentor model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_name_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_name.id'), nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    class_region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_region.id'), nullable=True)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group.id'), nullable=True)

    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id])
    class_name: so.Mapped['ClassName'] = so.relationship(foreign_keys=[class_name_id])
    class_batch: so.Mapped['ClassBatch'] = so.relationship(foreign_keys=[class_batch_id])
    class_region: so.Mapped['ClassRegion'] = so.relationship(foreign_keys=[class_region_id])
    class_group: so.Mapped['ClassGroup'] = so.relationship(foreign_keys=[class_group_id])

class UserStatusInbatch(BaseModel):
    """UserStatusInbatch model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group.id'), nullable=False)
    status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user_status_lookup.id'), nullable=False)

    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id])
    class_group: so.Mapped['ClassGroup'] = so.relationship(foreign_keys=[class_group_id])
    status: so.Mapped['UserStatusLookup'] = so.relationship(foreign_keys=[status_id])

class UserStatusLookup(db.Model):
    """UserStatus lookup table."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

class StudentGroup(BaseModel):
    """StudentGroup model."""
    __table_args__ = (sa.UniqueConstraint('user_id', 'class_group_id'), {'extend_existing': True})
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group.id'), nullable=False)
    index_no: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user_status_lookup.id'), nullable=False)

    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id])
    class_group: so.Mapped['ClassGroup'] = so.relationship(foreign_keys=[class_group_id])
    status: so.Mapped['UserStatusLookup'] = so.relationship(foreign_keys=[status_id])

class ClassBatchTeacher(BaseModel):
    """ClassBatchTeacher model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)

    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id])
    class_batch: so.Mapped['ClassBatch'] = so.relationship(foreign_keys=[class_batch_id])

class Role(db.Model):
    """Role lookup table."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)
    level: so.Mapped[int] = so.mapped_column(sa.Integer, unique=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

class UserRole(BaseModel):
    """UserRole model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('role.id'), index=True, nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True, nullable=False)
    class_region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_region.id'), nullable=True)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=True)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group.id'), nullable=True)

    role: so.Mapped['Role'] = so.relationship(foreign_keys=[role_id])
    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id])
    class_region: so.Mapped['ClassRegion'] = so.relationship(foreign_keys=[class_region_id])
    class_batch: so.Mapped['ClassBatch'] = so.relationship(foreign_keys=[class_batch_id])
    class_group: so.Mapped['ClassGroup'] = so.relationship(foreign_keys=[class_group_id])

class Message(BaseModel):
    """Message model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    body: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    sender: so.Mapped['User'] = so.relationship(foreign_keys=[sender_id])
    recipient: so.Mapped['User'] = so.relationship(foreign_keys=[recipient_id])

class File(BaseModel):
    """File model."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    data: so.Mapped[bytes] = so.mapped_column(sa.LargeBinary, nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)

    user: so.Mapped['User'] = so.relationship(foreign_keys=[user_id])

class Regions(db.Model):
    """Represents a region in the world."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    translations: so.Mapped[str] = so.mapped_column(sa.Text)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    def __repr__(self):
        return f'<Region {self.name}>'

class Subregions(db.Model):
    """Represents a subregion within a region."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    translations: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('regions.id'), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    region: so.Mapped['Regions'] = so.relationship()

    def __repr__(self):
        return f'<Subregion {self.name}>'

class Countries(db.Model):
    """Represents a country."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    iso3: so.Mapped[str] = so.mapped_column(sa.String(3), nullable=True)
    numeric_code: so.Mapped[str] = so.mapped_column(sa.String(3), nullable=True)
    iso2: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=True)
    phonecode: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    capital: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    currency: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    currency_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    currency_symbol: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    tld: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    native: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    region: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('regions.id'), nullable=True)
    subregion: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    subregion_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('subregions.id'), nullable=True)
    nationality: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    timezones: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    translations: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(10, 8), nullable=True)
    longitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(11, 8), nullable=True)
    emoji: so.Mapped[str] = so.mapped_column(sa.String(191), nullable=True)
    emojiU: so.Mapped[str] = so.mapped_column(sa.String(191), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    region_ref: so.Mapped['Regions'] = so.relationship(foreign_keys=[region_id])
    subregion_ref: so.Mapped['Subregions'] = so.relationship(foreign_keys=[subregion_id])

    def __repr__(self):
        return f'<Country {self.name}>'

class States(db.Model):
    """Represents a state within a country."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'), nullable=False)
    country_code: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=False)
    fips_code: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    iso2: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(191), nullable=True)
    level: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    parent_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    native: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    latitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(10, 8), nullable=True)
    longitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(11, 8), nullable=True)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=True, default=None)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    country: so.Mapped['Countries'] = so.relationship()

    def __repr__(self):
        return f'<State {self.name}>'

class Cities(db.Model):
    """Represents a city within a state."""
    __table_args__ = {'extend_existing': True}
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    state_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('states.id'), nullable=False)
    state_code: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    country_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('countries.id'), nullable=False)
    country_code: so.Mapped[str] = so.mapped_column(sa.String(2), nullable=False)
    latitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(10, 8), nullable=False)
    longitude: so.Mapped[float] = so.mapped_column(sa.DECIMAL(11, 8), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default='2014-01-01 12:01:01')
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    flag: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)
    wikiDataId: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True, default=None)

    state: so.Mapped['States'] = so.relationship(foreign_keys=[state_id])
    country: so.Mapped['Countries'] = so.relationship(foreign_keys=[country_id])

    def __repr__(self):
        return f'<City {self.name}>'