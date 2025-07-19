#
import json
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
# from app.forms import LoginForm, RegistrationForm
# from app.models import User
import app.forms as fo
import app.models as mo
from . import forms
# from flask_debugtoolbar import DebugToolbarExtension
from functions.parse_wa_text import parse_wa_text_fn

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
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(mo.User).where(mo.User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid email or password {form.email.data} {user.email}')
            # flash('Invalid email or password')
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
            d=parse_wa_text_fn(whatsapptext)
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


@app.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """Renders the password page."""
    form = forms.PasswordForm()
    if form.validate_on_submit():
        user = None
        if form.user_id.data:
            user = db.session.get(mo.User, form.user_id.data)
        elif form.name.data:
            user = db.session.scalar(sa.select(mo.User).where(mo.User.username.like(f'%{form.name.data}%')))
        elif form.email.data:
            user = db.session.scalar(sa.select(mo.User).where(mo.User.email.like(f'%{form.email.data}%')))

        if user:
            password = db.session.scalar(sa.select(mo.Password).where(mo.Password.user_id == user.id))
            if password:
                password.password_hash = generate_password_hash(form.password.data)
                flash(f'Password for <a href="{url_for('show_a_user', user_id=user.id)}">{user.id}</a> updated.')
            else:
                password = mo.Password(user_id=user.id, password_hash=generate_password_hash(form.password.data))
                db.session.add(password)
                flash(f'Password for <a href="{url_for('show_a_user', user_id=user.id)}">{user.id}</a> added.')
            db.session.commit()
            return redirect(url_for('password'))
        else:
            flash('User not found.')
    return render_template('password.html', title='Password', form=form)

@app.route('/location', methods=['GET', 'POST'])
@login_required
def location():
    """Renders the location page, which allows users to search for locations.

    Returns:
        A rendered template of the location page.
    """
    form = fo.LocationForm()
    return render_template('location.html', title='Location', form=form)

@app.route('/api/states/<country_name>')
@login_required
def api_states(country_name):
    """Provides a list of states for a given country.

    Args:
        country_name (str): The name of the country to get states for.

    Returns:
        A JSON response containing a list of states.
    """
    country = db.session.scalar(sa.select(mo.Countries).where(mo.Countries.name.ilike(f'%{country_name}%')))
    if country:
        states = db.session.scalars(sa.select(mo.States).where(mo.States.country_id == country.id)).all()
        return jsonify([{'id': state.id, 'name': state.name} for state in states])
    return jsonify([])

@app.route('/api/cities/<country_name>/<int:state_id>')
@login_required
def api_cities(country_name, state_id):
    """Provides a list of cities for a given country and state.

    Args:
        country_name (str): The name of the country.
        state_id (int): The ID of the state.

    Returns:
        A JSON response containing a list of cities.
    """
    country = db.session.scalar(sa.select(mo.Countries).where(mo.Countries.name.ilike(f'%{country_name}%')))
    if country:
        cities = db.session.scalars(sa.select(mo.Cities).where(mo.Cities.country_id == country.id, mo.Cities.state_id == state_id)).all()
        return jsonify([{'id': city.id, 'name': city.name} for city in cities])
    return jsonify([])

@app.route('/api/location/<int:city_id>')
@login_required
def api_location(city_id):
    """Provides location data for a given city.

    Args:
        city_id (int): The ID of the city.

    Returns:
        A JSON response containing the location data.
    """
    city = db.session.get(mo.Cities, city_id)
    if city:
        # tz = [d['gmtOffsetName'] for d in json.loads(city.country.timezones)]
        return jsonify([{
            'Country': city.country.name,
            'ISO3': city.country.iso3,
            'ISO2': city.country.iso2,
            # 'Numeric Code': city.country.numeric_code,
            'Phone Code': city.country.phonecode,
            'Currency': city.country.currency,
            'Currency Name': city.country.currency_name,
            'Capital': city.country.capital,
            # 'Timezones': ','.join([d['gmtOffsetName']+'|'+d['abbreviation'] for d in json.loads(city.country.timezones)]),
            'Timezones': city.country.timezones,
            # 'Nationality': city.country.nationality,
            # 'Flag': city.country.flag,
            'CityState': city.state.name,
            'City': city.name,
            # 'Latitude': city.latitude,
            # 'Longitude': city.longitude
        }])
    return jsonify([])

