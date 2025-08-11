# app/forms.py
"""
This module defines the forms used throughout the Flask application.

It includes forms for user authentication (login, password), data entry for
various models like ClassName, ClassBatch, ClassRegion, etc., and other
specialized forms like WhatsApp registration and file uploads. The forms
are built using Flask-WTF and WTForms, and they include validators to ensure
the integrity of the submitted data.
"""
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField, BooleanField, TextAreaField, DateField, FileField, EmailField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional,InputRequired, NumberRange


import sqlalchemy as sa
from app import db
from app.models import User, ClassName, ClassBatch, ClassRegion, ClassGroup, ClassGroupMentor, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus, Countries, UserStatusLookup, Contact, RegStatusLookup

from .config import Config

thisyear = datetime.datetime.now().year

class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    captcha = StringField('Captcha', validators=[DataRequired()])
    register = SubmitField('Sign In')

class SupportForm(FlaskForm):
    """Support Form"""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    captcha = StringField('Captcha', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class PasswordForm(FlaskForm):
    """ Password Form """
    user_id = IntegerField('User ID', validators=[])
    name = StringField('Name', validators=[])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BatchForm(FlaskForm):
    """ select a class and batc to generate its registration template """
    class_name = SelectField('Class Name', choices=[])
    batch_name = SelectField('Class Batch', choices=[])
    submit = SubmitField('Generate Registration Template')


class RegFromWaText(FlaskForm):
    """ WhatsApp Registration Form """
    whatsapptext = TextAreaField('Paste WhatsApp Registration Text in the below box.', validators=[], render_kw={"rows": 34, "cols": 100})
    register = SubmitField('Register')

class UserRegForm(FlaskForm):
    """
    A form for registering new users.

    This form collects all the necessary information for creating a new user,
    including personal details, contact information, and batch selection.
    The batch choices are dynamically populated from the ClassBatch model.
    """
    class_name = SelectField('Select Class', coerce=int, validators=[DataRequired()])
    batch_name = SelectField('Select Batch', coerce=int, validators=[DataRequired()])
    
    full_name = StringField('Full Name', validators=[DataRequired()], description='Full name of new user being registered')
    mobile = StringField('Mobile With Country Code', validators=[DataRequired()], description='No symbol or white space. Only integer e.g. 911234567890')
    whatsapp = StringField('WhatsApp With Country Code', validators=[DataRequired()], description='No symbol or white space. Only integer e.g. 911234567890')
    email = EmailField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[('M', 'M'), ('F', 'F')], validators=[DataRequired()], description='M or F')
    
    hometown_country = SelectField('Hometown Country', coerce=int, validators=[DataRequired()])
    hometown_state = SelectField('Hometown State', coerce=int, validators=[DataRequired()])
    hometown_district = SelectField('Hometown District', coerce=int, validators=[DataRequired()])
    hometown_city = StringField('Hometown City', validators=[Length(max=32)])

    resident_country = SelectField('Current Residence Country', coerce=int, validators=[DataRequired()])
    resident_state = SelectField('Current Residence State', coerce=int, validators=[DataRequired()])
    resident_city = SelectField('Current Residence City', coerce=int, validators=[DataRequired()])

    yob             = IntegerField('Year of Birth', validators=[InputRequired(), NumberRange(min=thisyear - 80, max=thisyear - 10, message="Birthday is not in range or invalid.")])
    education       = TelField('Highest Education', validators=[DataRequired()])
    profession      = TelField('Profession', validators=[DataRequired()])
    
    referrer_name   = TelField('Referrer Name', validators=[])
    referrer_mobile = StringField('Referrer Mobile', validators=[DataRequired()], description='No symbol or white space. Only integer e.g. 911234567890')
    referrer_email = EmailField('Referrer Email', validators=[DataRequired(), Email()])
    referrer_batch = StringField('Referrer Batch', validators=[Length(max=32)])
    referrer_student_id = IntegerField('Referrer Student ID', validators=[Optional()])

    any_other_detail    = TextAreaField('Any Other Detail', validators=[], render_kw={"rows": 2, "cols": 80}) 
    registration_status = SelectField('Registration Status', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(UserRegForm, self).__init__(*args, **kwargs)
        self.hometown_country.choices = [(c.id, c.name) for c in Countries.query.order_by(Countries.name).all()]
        self.resident_country.choices = [(c.id, c.name) for c in Countries.query.order_by(Countries.name).all()]
        
        self.hometown_state.choices = []
        self.hometown_district.choices = []
        self.resident_state.choices = []
        self.resident_city.choices = []
  
        self.class_name.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.batch_name.choices = []

        # Set default value for registration_status
        reg_status = RegStatusLookup.query.filter_by(status='NewRegistration').first()
        if reg_status:
            self.registration_status.choices = [(reg_status.id, reg_status.status)]
            self.registration_status.data = reg_status.id
        else:
            self.registration_status.choices = [(s.id, s.status) for s in RegStatusLookup.query.all()]

    def validate_email_mobile(self, email, mobile):
        """Validate that the email or mobile number is unique."""
        user = User.query.filter((User.email == self.email.data) | (User.mobile == self.mobile.data)).first()
        if user:
            raise ValidationError('A user with that email or mobile number already exists.')




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
    """
    A form for creating and updating ClassRegion objects.

    This form includes fields for selecting a class name and a class batch,
    and for entering a section and a description. The class batch dropdown
    is populated dynamically based on the selected class name.
    """
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired(), Length(max=1)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """
        Initializes the ClassRegionForm.

        It populates the 'class_name_id' dropdown with all available class names
        and leaves the 'class_batch_id' dropdown empty, to be populated
        dynamically.
        """
        super(ClassRegionForm, self).__init__(*args, **kwargs)
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.class_batch_id.choices = []

class ClassGroupForm(FlaskForm):
    """ClassGroup Form"""
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    class_region_id = SelectField('Class Region', coerce=int, validators=[DataRequired()])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    start_index = IntegerField('Start Index', validators=[Optional()])
    end_index = IntegerField('End Index', validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        super(ClassGroupForm, self).__init__(*args, **kwargs)
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
        self.class_group_id.choices = [(g.id, g.description) for g in ClassGroup.query.all()]

class UserStatusForm(FlaskForm):
    """UserStatus Form"""
    status = StringField('Status', validators=[DataRequired(), Length(max=16)])
    description = StringField('Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Submit')

class StudentGroupForm(FlaskForm):
    """StudentGroup Form"""
    user_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    class_group_id = SelectField('Class Group', coerce=int, validators=[DataRequired()])
    index_no = IntegerField('Index No', validators=[Optional()])
    status_id = SelectField('Status', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        super(StudentGroupForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.class_group_id.choices = [(g.id, g.description) for g in ClassGroup.query.all()]
        self.status_id.choices = [(s.id, s.status) for s in UserStatusLookup.query.all()]

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
    class_name_id = SelectField('Class Name', coerce=int, validators=[DataRequired()])
    class_batch_id = SelectField('Class Batch', coerce=int, validators=[DataRequired()])
    class_region_id = SelectField('Class Region', coerce=lambda x: int(x) if x and x != 'None' else None, validators=[Optional()])
    class_group_id = SelectField('Class Group', coerce=lambda x: int(x) if x and x != 'None' else None, validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        """Initialize the form"""
        super(UserRoleForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.username) for u in User.query.all()]
        self.role_id.choices = [(r.id, r.role) for r in Role.query.order_by(Role.level).all()]
        self.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.class_batch_id.choices = []
        self.class_region_id.choices = [(None, 'All Regions')]
        self.class_group_id.choices = [(g.id, g.description) for g in ClassGroup.query.all()]

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

class EmptyForm(FlaskForm):
    """An empty form for CSRF protection."""
    pass

class SearchUserForm(FlaskForm):
    """Search User Form"""
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class AdminChangePasswordForm(FlaskForm):
    """Admin Change Password Form"""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    is_allowed = BooleanField('Is Allowed')
    force_change = BooleanField('Force Change')
    submit = SubmitField('Update Password')


class ChangePasswordForm(FlaskForm):
    """Change Password Form"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm_new_password', message='Passwords must match')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class UserSearchForm(FlaskForm):
    """User Search Form"""
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class SearchClassGroupForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class ReferrerSearchForm(FlaskForm):
    """Referrer search form."""
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class UpdateReferrerForm(FlaskForm):
    """Update referrer form."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=64)])
    mobile = IntegerField('Mobile')
    email = StringField('Email', validators=[Email(), Length(max=120)])
    batch = StringField('Batch', validators=[Length(max=16)])
    referrer_id = IntegerField('Referrer ID')
    submit = SubmitField('Update')