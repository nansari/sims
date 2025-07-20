
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
import sqlalchemy as sa
from app import db
from app.models import User, ClassName, ClassBatch, ClassRegion, ClassGroupIndex, ClassGroupMentor, UserStatus, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus

class ClassNameForm(FlaskForm):
    """ClassName Form"""
    name = StringField('Name', validators=[DataRequired(), Length(max=8)])
    submit = SubmitField('Submit')

class ClassBatchForm(FlaskForm):
    """ClassBatch Form"""
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    batch_no = StringField('Batch No', validators=[DataRequired(), Length(max=3)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    status_id = SelectField('Status', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ClassBatchForm, self).__init__(*args, **kwargs)
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.status_id.choices = [(s.id, s.status) for s in ClassBatchStatus.query.all()]

class ClassRegionForm(FlaskForm):
    """ClassRegion Form"""
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired(), Length(max=1)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ClassRegionForm, self).__init__(*args, **kwargs)
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]

class ClassGroupIndexForm(FlaskForm):
    """ClassGroupIndex Form"""
    class_region_id = SelectField('Class Region', coerce=int, validators=[DataRequired()])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    start_index = IntegerField('Start Index', validators=[Optional()])
    end_index = IntegerField('End Index', validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ClassGroupIndexForm, self).__init__(*args, **kwargs)
        self.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.all()]

class ClassGroupMentorForm(FlaskForm):
    """ClassGroupMentor Form"""
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    class_region_id = SelectField('Class Region', coerce=int, validators=[Optional()])
    class_group_id = SelectField('Class Group', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ClassGroupMentorForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]
        self.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.all()]
        self.class_group_id.choices = [(g.id, g.description) for g in ClassGroupIndex.query.all()]

class UserStatusForm(FlaskForm):
    """UserStatus Form"""
    status = StringField('Status', validators=[DataRequired(), Length(max=16)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Submit')

class StudentGroupForm(FlaskForm):
    """StudentGroup Form"""
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    class_group_id = SelectField('Class Group', coerce=int, validators=[DataRequired()])
    index_no = IntegerField('Index No', validators=[Optional()])
    status_id = SelectField('Status', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(StudentGroupForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.class_group_id.choices = [(g.id, g.description) for g in ClassGroupIndex.query.all()]
        self.status_id.choices = [(s.id, s.status) for s in UserStatus.query.all()]

class ClassBatchTeacherForm(FlaskForm):
    """ClassBatchTeacher Form"""
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ClassBatchTeacherForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]

class RoleForm(FlaskForm):
    """Role Form"""
    role = StringField('Role', validators=[DataRequired(), Length(max=16)])
    level = IntegerField('Level', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Submit')

class UserRoleForm(FlaskForm):
    """UserRole Form"""
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()])
    class_region_id = SelectField('Class Region', coerce=int, validators=[Optional()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[Optional()])
    class_group_id = SelectField('Class Group', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.role_id.choices = [(r.id, r.role) for r in Role.query.all()]
        self.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.all()]
        self.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]
        self.class_group_id.choices = [(g.id, g.description) for g in ClassGroupIndex.query.all()]

class ClassBatchStatusForm(FlaskForm):
    """ClassBatchStatus Form"""
    status = StringField('Status', validators=[DataRequired(), Length(max=16)])
    submit = SubmitField('Submit')
