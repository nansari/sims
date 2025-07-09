#
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
# from app.forms import LoginForm, RegistrationForm
# from app.models import User
import app.forms as fo
import app.models as mo
from . import forms
from functions import parse_wa_text
# from flask_debugtoolbar import DebugToolbarExtension

# @app.route('/home')
@app.route('/')
@app.route('/index')
@login_required
def index():
    """Renders the home page."""
    # user = {'username': 'Nasim'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = fo.LoginForm()
    if form.validate_on_submit():#zzzz
        user = db.session.scalar(
            sa.select(mo.User).where(mo.User.username == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Renders the logout page"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/reg_template', methods=['GET', 'POST'])
def reg_template():
    """Renders the reg_template page"""
    # selected_batch = redirect(url_for('select_a_batch'))
    # print(selected_batch.data)
    form = fo.BatchForm()
    if form.validate_on_submit():
        # render_template('select_batch.html', form=form)
        # selected_batch = form.batch.data
        select_a_batch = request.form.get('batch')
        return render_template('reg_template.html', batch=select_a_batch)

    return render_template('select_batch.html', form=form)


@app.route('/select_a_batch', methods=['GET', 'POST'])
@login_required
def select_a_batch():
    """Renders the select_a_batch page"""
    form = forms.BatchForm()
    
    # # Fetch predefined batches from the database
    # form.batch.choices = [(batch.id, batch.name) for batch in Batch.query.all()]  # Adjust according to your model

    form = forms.BatchForm()
    if form.validate_on_submit():
        # render_template('select_batch.html', form=form)
        # selected_batch = form.batch.data
        select_a_batch = request.form.get('batch')
        return render_template('batch_selected.html', batch=select_a_batch)
    if form.validate_on_submit():
        pass
    return render_template('select_batch.html', form=form)

        # WORKING CODE
        # whatsapptext = request.form.get('whatsapptext')
        # d=parse_wa_text(whatsapptext)
        # form = forms.UserRegForm(data=d)
        # return render_template('user_reg.html', form=form)

@app.route('/reg_from_wa_text', methods=['GET', 'POST'])
def reg_from_wa_text():
    """Render the reg_from_wa_text page to accept WhatsApp text."""
    form = forms.RegFromWaText()
    if form.validate_on_submit():
        whatsapptext = request.form.get('whatsapptext')
        if whatsapptext:
            d=parse_wa_text(whatsapptext)
            form = forms.UserRegForm(data=d)
            return render_template('user_reg.html', form=form)
        else:
            flash("Student data is submitted and redirecting")
            return render_template('reg_from_wa_text.html', form=form)
            # return redirect(url_for('user_reg', **request.form))
    
        #
        # whatsapptext = request.form.get('whatsapptext')
        # d=parse_wa_text(whatsapptext)
        # form = forms.UserRegForm(data=d)
        # return render_template('user_reg.html', form=form)
        #
        # return render_template('reg_from_wa_text.html', batch=select_a_batch)
        # return render_template('batch_selected.html', batch=parse_wa_text(whatsapptext))
        # form.name.data = "this is mny NAME"

        # if whatsapptext:
        #     d=parse_wa_text(whatsapptext)
        #     return render_template('user_reg.html', **d)
        #     # return redirect(url_for('user_reg', **d))
        # return render_template('reg_from_wa_text.html', form=form)
        # else:
        #     # TODO: save to database
        #     print("Student data is:", request.form)
        #     return redirect(url_for('reg_from_wa_text'))
    if form.validate_on_submit():
        pass
    return render_template('reg_from_wa_text.html', form=form)

import requests

@app.route('/support', methods=['GET', 'POST'])
def support():
    """Renders the support page."""
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        if recaptcha_response:
            payload = {
                'secret': '6LeYgH0rAAAAAIOfXv_P6TERJpilLaliTLxxBjfv',
                'response': recaptcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
            result = response.json()
            if result.get('success'):
                # Handle form submission
                flash('Your support request has been submitted successfully!')
                return redirect(url_for('index'))
            else:
                flash('reCAPTCHA verification failed. Please try again.')
        else:
            flash('Please complete the reCAPTCHA.')
    return render_template('support.html')

@app.route('/user_reg', methods=['GET', 'POST'])
@login_required
def user_reg():
    """Renders the user_reg page"""
    form = forms.UserRegForm()
    a_form_submitted = False
    if form.validate_on_submit(): # True only for POST Methos
        user = mo.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, the user is registered!')
        # request.args is ImmutableMultiDict([]) 
        # request.form is :ImmutableMultiDict([('csrf_token', 'ac'), ('batch', 'KARAMA-08'), ('email', 'adsfa@sdfsd.com'), ('name', 'asdf'), ('gender', 'M'), ('yob', '1980'), ('mobile', '987979879'), ('hometowncity', '987979879'), ('hometowncity', '987979879'), ('hometowndistrict', 'sdf'), ('hometownstate', 'sdf'), ('hometowncountry', 'sdf'), ('residencecity', 'sdf'), ('residencestate', 'asdf'), ('residentcountry', 'sdf'), ('residentzip', '2343'), ('education', 'sdf'), ('profession', 'asdf'), ('referrer_id', '344'), ('status', 'CallOut'), ('bio', 'wqerwe'), ('submit', 'Submit')])
        # flash("User is registered with data request.args {} request.form:{}".format( request.args, request.form))
        a_form_submitted = True    
    return render_template('user_reg.html', a_form_submitted=a_form_submitted, form=form)


@app.route('/show_a_user/<user_id>', methods=['GET', 'POST'])
@login_required
def show_a_user(user_id):
    """Renders the show_a_user page"""
    # return f"<html><body><p>Display user details of {user_id}</p></body></html>"
    return render_template('show_a_user.html', user_id=user_id)

