
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone

class BaseModel(db.Model):
    """Base model for other models to inherit from."""
    __abstract__ = True
    created_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_by: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class ClassName(BaseModel):
    """ClassName model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(8), unique=True, nullable=False)

class ClassBatchStatus(db.Model):
    """ClassBatchStatus lookup table."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)

class ClassBatch(BaseModel):
    """ClassBatch model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_name_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_name.id'), nullable=False)
    batch_no: so.Mapped[str] = so.mapped_column(sa.String(3), nullable=False)
    start_date: so.Mapped[datetime] = so.mapped_column(nullable=False)
    status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch_status.id'), nullable=False)

    class_name: so.Mapped['ClassName'] = so.relationship()
    status: so.Mapped['ClassBatchStatus'] = so.relationship()

class ClassRegion(BaseModel):
    """ClassRegion model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_name_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_name.id'), nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    section: so.Mapped[str] = so.mapped_column(sa.String(1), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

    class_name: so.Mapped['ClassName'] = so.relationship()
    class_batch: so.Mapped['ClassBatch'] = so.relationship()

class ClassGroupIndex(BaseModel):
    """ClassGroupIndex model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    class_region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_region.id'), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    start_index: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    end_index: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    class_region: so.Mapped['ClassRegion'] = so.relationship()

class ClassGroupMentor(BaseModel):
    """ClassGroupMentor model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_name_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_name.id'), nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)
    class_region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_region.id'), nullable=True)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group_index.id'), nullable=True)

    user: so.Mapped['User'] = so.relationship()
    class_name: so.Mapped['ClassName'] = so.relationship()
    class_batch: so.Mapped['ClassBatch'] = so.relationship()
    class_region: so.Mapped['ClassRegion'] = so.relationship()
    class_group: so.Mapped['ClassGroupIndex'] = so.relationship()

class UserStatus(db.Model):
    """UserStatus lookup table."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

class StudentGroup(BaseModel):
    """StudentGroup model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    student_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group_index.id'), nullable=False)
    index_no: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    status_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user_status.id'), nullable=False)

    student: so.Mapped['User'] = so.relationship()
    class_group: so.Mapped['ClassGroupIndex'] = so.relationship()
    status: so.Mapped['UserStatus'] = so.relationship()
    __table_args__ = (sa.UniqueConstraint('student_id', 'class_group_id'),)

class ClassBatchTeacher(BaseModel):
    """ClassBatchTeacher model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), nullable=False)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=False)

    user: so.Mapped['User'] = so.relationship()
    class_batch: so.Mapped['ClassBatch'] = so.relationship()

class Role(db.Model):
    """Role lookup table."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(16), unique=True, nullable=False)
    level: so.Mapped[int] = so.mapped_column(sa.Integer, unique=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)

class UserRole(BaseModel):
    """UserRole model."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('role.id'), index=True, nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'), index=True, nullable=False)
    class_region_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_region.id'), nullable=True)
    class_batch_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_batch.id'), nullable=True)
    class_group_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('class_group_index.id'), nullable=True)

    role: so.Mapped['Role'] = so.relationship()
    user: so.Mapped['User'] = so.relationship()
    class_region: so.Mapped['ClassRegion'] = so.relationship()
    class_batch: so.Mapped['ClassBatch'] = so.relationship()
    class_group: so.Mapped['ClassGroupIndex'] = so.relationship()
