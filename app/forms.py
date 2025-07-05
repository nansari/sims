# app/forms.py
import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TelField, TextAreaField, EmailField, StringField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length

# from app import app

from .config import Config

thisyear = datetime.datetime.now().year

class BatchForm(FlaskForm):
    """ Batch Selection Form """
    # batch = SelectField('Select Batch', choices=Config.BATCHES, coerce=str)
    batch = SelectField('Select Batch', choices=Config.BATCHES)
    submit = SubmitField('Submit')

class RegFromWaText(FlaskForm):
    """ WhatsApp Registration Form """
    whatsapptext = TextAreaField('Paste WhatsApp Registration Form', validators=[], render_kw={"rows": 35, "cols": 80})
    submit = SubmitField('Submit')

class UserRegForm(FlaskForm):
    """ User Registration Form """
    batch           = SelectField('Select Batch', choices=Config.BATCHES, default=Config.BATCHES[-1])
    email           = EmailField('Email', validators=[DataRequired()])
    name            = TelField('Name', validators=[DataRequired()])
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
    submit          = SubmitField('Submit')  

