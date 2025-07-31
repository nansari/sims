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
from app.models import User, ClassName, ClassBatch, ClassRegion, ClassGroup, ClassGroupMentor, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus, Countries, UserStatusLookup, Contact

from .config import Config

thisyear = datetime.datetime.now().year

class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    register = SubmitField('Sign In')
    
class PasswordForm(FlaskForm):
    """ Password Form """
    user_id = IntegerField('User ID', validators=[])
    name = StringField('Name', validators=[])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class BatchForm(FlaskForm):
    """
    A form for selecting a batch.

    This form provides a dropdown field to select a class batch. The choices
    are dynamically populated from the ClassBatch model.
    """
    batch = SelectField('Select Batch', coerce=int)
    submit = SubmitField('Generate')

    def __init__(self, *args, **kwargs):
        """
        Initializes the BatchForm.

        It populates the 'batch' dropdown with all available class batches.
        """
        super(BatchForm, self).__init__(*args, **kwargs)
        self.batch.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]


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
    # batch 
    classname           = SelectField('Select Class', coerce=int) # GLB, HYD
    classbatch           = SelectField('Select Batch', coerce=int) # B01
    # personal details
    username        = TelField('Name', validators=[DataRequired()])
    mobile          = IntegerField('Mobile with country code', validators=[DataRequired()])
    whatsapp        = IntegerField('WhatsApp with country code', validators=[DataRequired()])
    
    email           = EmailField('Email', validators=[DataRequired(), Email()])
    gender          = SelectField('Gender', choices=Config.GENDERS, validators=[])
    # HOMETOWN DETAILS
    hometowncountry = SelectField('Hometown Country', coerce=int, validators=[DataRequired()])
    hometownstate   = TelField('Hometown State', validators=[DataRequired()])
    hometowndistrict = TelField('Hometown District', validators=[DataRequired()])
    hometowncity    = TelField('Hometown City', validators=[DataRequired()])
    hometownzip     = TelField('Hometown Pin/Zip', validators=[])
    # RESIDENCE DETAILS
    residentcountry = SelectField('Current Residence Country', coerce=int, validators=[DataRequired()])
    residencestate  = TelField('Current Residence State', validators=[DataRequired()])
    residencecity   = TelField('Current Residence City', validators=[DataRequired()])
    residencearea   = TelField('Area in Residence City', validators=[DataRequired()])
    residentzip     = TelField('Current Residence Pin/Zip', validators=[])
    # OTHER DETAILS
    yob             = IntegerField('Year of Birth', validators=[InputRequired(), NumberRange(min=thisyear - 80, max=thisyear - 10, message="Birthday is not in range or invalid.")])
    education       = TelField('Highest Education', validators=[DataRequired()])
    profession      = TelField('Profession', validators=[DataRequired()])
    # referral and status
    referrer_name   = TelField('Referred By Name', validators=[])
    referrer_mobile = IntegerField('Referred By Mobile', validators=[], default=0)
    bio             = TextAreaField('Notes', validators=[], render_kw={"rows": 2, "cols": 80})    
    # referrer_id     = IntegerField('Referred By ID', validators=[], default=0)
    # Additional fields and submit
    status          = SelectField('Status', coerce=int, validators=[], default=1) # Registration
    register        = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserRegForm.

        It populates the 'batch' dropdown with all available class batches.
        """
        super(UserRegForm, self).__init__(*args, **kwargs)
        self.classname.choices = [(c.id, c.name) for c in ClassName.query.all()]
        self.classbatch.choices = [(b.id, b.batch_no) for b in ClassBatch.query.all()]
        self.hometowncountry.choices = [(c.id, c.name) for c in Countries.query.order_by(Countries.name).all()]
        self.residentcountry.choices = [(c.id, c.name) for c in Countries.query.order_by(Countries.name).all()]
        self.status.choices = [(s.id, s.status) for s in UserStatusLookup.query.all()]

    def validate_username(self, username):
        """Validate username"""
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    

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


