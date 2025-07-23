# app/forms.py
"""
This module contains the forms for the application.
"""
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField, BooleanField, TextAreaField, DateField, FileField, EmailField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional,InputRequired, NumberRange

import sqlalchemy as sa
from app import db
from app.models import User, ClassName, ClassBatch, ClassRegion, ClassGroupIndex, ClassGroupMentor, UserStatus, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus

from .config import Config

thisyear = datetime.datetime.now().year

class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    register = SubmitField('Sign In')
    
class PasswordForm(FlaskForm):
    """ Password Form """
    user_id = IntegerField('User ID', validators=[])
    name = StringField('Name', validators=[])
    email = StringField('Email', validators=[])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class BatchForm(FlaskForm):
    """ Batch Selection Form """
    # batch = SelectField('Select Batch', choices=Config.BATCHES, coerce=str)
    batch = SelectField('Select Batch', choices=Config.BATCHES)
    submit = SubmitField('Generate')


class RegFromWaText(FlaskForm):
    """ WhatsApp Registration Form """
    whatsapptext = TextAreaField('Paste WhatsApp Registration Text in the below box.', validators=[], render_kw={"rows": 34, "cols": 100})
    register = SubmitField('Register')

class UserRegForm(FlaskForm):
    """ User Registration Form """
    batch           = SelectField('Select Batch', choices=Config.BATCHES, default=Config.BATCHES[-1])
    email           = EmailField('Email', validators=[DataRequired()])
    username        = TelField('Name', validators=[DataRequired()])
    visa_type       = TelField('Visa Type', validators=[])
    gender          = SelectField('Gender', choices=['M', 'F'], validators=[])
    yob             = IntegerField('Year of Birth', validators=[InputRequired(), NumberRange(min=thisyear - 80, max=thisyear - 10, message="Birthday is not in range or invalid.")])
    mobile          = IntegerField('Mobile with country code', validators=[DataRequired()])
    whatsapp        = IntegerField('WhatsApp with country code', validators=[DataRequired()])
    hometowncity    = TelField('Hometown City', validators=[DataRequired()])
    hometowndistrict = TelField('Hometown District', validators=[DataRequired()])
    hometownstate   = TelField('Hometown State', validators=[DataRequired()])
    hometowncountry = SelectField('Hometown Country', choices=Config.COUNTRIES, validators=[DataRequired()])
    residencecity   = TelField('Current Residence City', validators=[DataRequired()])
    residencestate  = TelField('Current Residence State', validators=[DataRequired()])
    residentcountry = SelectField('Current Residence Country', choices=Config.COUNTRIES, validators=[DataRequired()])
    residentzip     = TelField('Current Residence Pin/Zip', validators=[])
    education       = TelField('Highest Education', validators=[DataRequired()])
    profession      = TelField('Profession', validators=[DataRequired()])
    referrer_id     = IntegerField('Referred By ID', validators=[], default=0)
    status          = SelectField('Status', choices=Config.STATUS, default=Config.STATUS[0], validators=[])
    bio             = TextAreaField('Notes', validators=[], render_kw={"rows": 2, "cols": 80})    
    register        = SubmitField('Register')


    def validate_username(self, username):
        """Validate username"""
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Validate email"""
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LocationForm(FlaskForm):
    """A form for selecting a location by country, state, and city.

    Attributes:
        country (StringField): A text field for entering the country name.
        state (SelectField): A dropdown for selecting the state.
        city (SelectField): A dropdown for selecting the city.
        submit (SubmitField): A button to submit the form.
    """
    country = StringField('Country', validators=[DataRequired()])
    state = SelectField('State', choices=[], validators=[DataRequired()])
    city = SelectField('City', choices=[], validators=[DataRequired()])
    submit = SubmitField('Search')


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
        """Initialize the form"""
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
        """Initialize the form"""
        super(ClassRegionForm, self).__init__(*args, **kwargs)
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]

class ClassGroupIndexForm(FlaskForm):
    """ClassGroupIndex Form"""
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    class_region_id = SelectField('Class Region', coerce=int, validators=[DataRequired()])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    start_index = IntegerField('Start Index', validators=[Optional()])
    end_index = IntegerField('End Index', validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        super(ClassGroupIndexForm, self).__init__(*args, **kwargs)
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.class_batch_id.choices = []
        self.class_region_id.choices = []

class ClassGroupMentorForm(FlaskForm):
    """ClassGroupMentor Form"""
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    class_region_id = SelectField('Class Region', coerce=int, validators=[Optional()])
    class_group_id = SelectField('Class Group', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
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
        """Initialize the form"""
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
        """Initialize the form"""
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
        """Initialize the form"""
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

class MessageForm(FlaskForm):
    """Message Form"""
    recipient = StringField('Recipient', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Send')

class FileUploadForm(FlaskForm):
    """File Upload Form"""
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')

