# app/routes.py
"""
This module defines the routes for the Flask application.

It includes routes for user authentication (login, logout), registration,
and various functionalities related to managing classes, batches, regions,
groups, and other application-specific data. It also defines API endpoints
for fetching data dynamically.
"""
import json
from urllib.parse import urlsplit
import json
import time
import logging
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, send_file, jsonify, current_app, session
from app.config import Config

# Configure logging
logging.basicConfig(filename=Config.LOGFILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
from io import BytesIO
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import db, captcha
from app.forms import ClassNameForm, ClassBatchForm, ClassRegionForm, ClassGroupForm, ClassGroupMentorForm, UserStatusForm, StudentGroupForm, ClassBatchTeacherForm, RoleForm, UserRoleForm, ClassBatchStatusForm, BatchForm, ReferrerSearchForm, UpdateReferrerForm
from app.models import ClassName, ClassBatch, ClassRegion, ClassGroup, ClassGroupMentor, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus, UserStatusLookup, RegStatusLookup, Referrer
# from app.forms import LoginForm, RegistrationForm
# from app.models import User
import app.forms as fo
import app.models as mo
from . import forms
# from flask_debugtoolbar import DebugToolbarExtension
from functions.parse_wa_text import parse_wa_text_fn
from werkzeug.security import generate_password_hash, check_password_hash


@current_app.route('/')
@current_app.route('/index')
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


@current_app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = fo.LoginForm()
    if form.validate_on_submit():
        if captcha.validate():
            user = db.session.scalar(
                sa.select(mo.User).join(mo.User.contact).where(mo.Contact.email == form.email.data))
            
            if not user:
                flash('Invalid email or password', 'danger')
                logging.info(f"Login denied: Invalid email or password for email: {form.email.data} from IP: {request.remote_addr} User-Agent: {request.user_agent}") # Log denied
                return redirect(url_for('login'))

            password_hash = db.session.scalar(sa.select(mo.Password).where(mo.Password.user_id == user.id))

            if not password_hash or not mo.Password.check_password(password_hash, form.password.data):
                flash('Invalid email or password', 'danger')
                logging.info(f"Login denied: Invalid email or password for email: {form.email.data} from IP: {request.remote_addr} User-Agent: {request.user_agent}") # Log denied
                return redirect(url_for('login'))

            login_user(user, remember=form.remember_me.data)
            logging.info(f"Login successful for user: {user.username} (email: {form.email.data}) from IP: {request.remote_addr} User-Agent: {request.user_agent}") # Log successful
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid captcha. Please try again.', 'danger')
            logging.info(f"Login denied: Invalid captcha for email: {form.email.data} from IP: {request.remote_addr} User-Agent: {request.user_agent}") # Log denied
    return render_template('login.html', title='Sign In', form=form)

@login_required
@current_app.route('/logout')
def logout():
    """Renders the logout page"""
    logout_user()
    return redirect(url_for('index'))


@current_app.route('/reg_template', methods=['GET', 'POST'])
@login_required
def reg_template():
    """Renders the reg_template page"""
    form = fo.BatchForm()
    form.class_name.choices = [(c.id, c.name) for c in ClassName.query.all()]
    form.class_name.choices.insert(0, (0, 'Select Class Name'))

    if request.method == 'POST':
        class_name_id = form.class_name.data
        if class_name_id:
            form.batch_name.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=class_name_id).all()]
        else:
            form.batch_name.choices = []
        form.batch_name.choices.insert(0, (0, 'Select Class Batch'))

    if form.validate_on_submit():
        class_name_id = form.class_name.data
        batch_name_id = form.batch_name.data
        class_name = ClassName.query.get(class_name_id)
        batch = ClassBatch.query.get(batch_name_id)
        return render_template('display_template.html', title=f'{class_name.name}-{batch.batch_no} Registration Template', class_name=class_name.name, batch_no=batch.batch_no)

    return render_template('reg_template.html', title='Registration Template', form=form)


@current_app.route('/get_batches/<int:class_id>')
@login_required
def get_batches(class_id):
    batches = ClassBatch.query.filter_by(class_name_id=class_id).all()
    batch_list = [{'id': batch.id, 'name': batch.batch_no} for batch in batches]
    return jsonify({'batches': batch_list})


@current_app.route('/select_a_batch', methods=['GET', 'POST'])
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

@current_app.route('/reg_from_wa_text', methods=['GET', 'POST'])
@login_required
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


@current_app.route('/support', methods=['GET', 'POST'])
def support():
    """Renders the support page."""
    form = fo.SupportForm()
    if form.validate_on_submit():
        if captcha.validate():
            # Handle form submission
            flash('Your support request has been submitted successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid captcha. Please try again.', 'danger')
    return render_template('support.html', form=form)

@current_app.route('/user_reg', methods=['GET', 'POST'])
@login_required
def user_reg():
    """Renders the user_reg page"""
    form = forms.UserRegForm()
    if form.validate_on_submit():
        user = mo.User(
            full_name=form.full_name.data,
            mobile=form.mobile.data,
            whatsapp=form.whatsapp.data,
            email=form.email.data,
            gender=form.gender.data,
            hometown_country_id=form.hometown_country.data,
            hometown_state_id=form.hometown_state.data,
            hometown_district_id=form.hometown_district.data,
            hometown_city=form.hometown_city.data,
            resident_country_id=form.resident_country.data,
            resident_state_id=form.resident_state.data,
            resident_city_id=form.resident_city.data,
            user_status_id=form.registration_status.data,
            referrer_mobile=form.referrer_mobile.data,
            referrer_email=form.referrer_email.data,
            referrer_student_id=form.referrer_student_id.data,
            created_by=current_user.id,
            updated_by=current_user.id
        )
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, the user is registered!')
        return redirect(url_for('user_reg'))
    return render_template('user_reg.html', form=form)


@current_app.route('/api/batches_for_class/<int:class_id>')
def batches_for_class(class_id):
    batches = ClassBatch.query.filter_by(class_name_id=class_id).all()
    return jsonify([{'id': batch.id, 'name': batch.batch_no} for batch in batches])


@current_app.route('/api/states_for_country/<int:country_id>')
def states_for_country(country_id):
    states = mo.States.query.filter_by(country_id=country_id).all()
    return jsonify([{'id': state.id, 'name': state.name} for state in states])


@current_app.route('/api/cities_for_state/<int:state_id>')
def cities_for_state(state_id):
    cities = mo.Cities.query.filter_by(state_id=state_id).all()
    return jsonify([{'id': city.id, 'name': city.name} for city in cities])


@current_app.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """Renders the password page."""
    form = fo.UserSearchForm()
    users = []
    if form.validate_on_submit():
        search_term = form.search.data
        users = db.session.query(mo.User).join(mo.User.contact).filter(
            sa.or_(
                mo.User.username.ilike(f'%{search_term}%'),
                mo.Contact.email.ilike(f'%{search_term}%')
            )
        ).all()
    return render_template('password.html', title='Password', form=form, users=users)

@current_app.route('/set_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def set_password(user_id):
    """Renders the set_password page."""
    user = db.session.get(mo.User, user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('password'))
    form = fo.AdminChangePasswordForm()
    if form.validate_on_submit():
        password = db.session.scalar(sa.select(mo.Password).where(mo.Password.user_id == user.id))
        profile_url = url_for('user_profile', username=user.username)
        if password:
            password.password_hash = generate_password_hash(form.password.data)
            flash(f'Password for <a href="{profile_url}">{user.username}</a> updated.')
        else:
            password = mo.Password(user_id=user.id, password_hash=generate_password_hash(form.password.data))
            db.session.add(password)
            flash(f'Password for <a href="{profile_url}">{user.username}</a> added.')
        db.session.commit()
        return redirect(url_for('password'))
    return render_template('set_password.html', title='Set Password', form=form, user=user)

@current_app.route('/location', methods=['GET', 'POST'])
@login_required
def location():
    """Renders the location page, which allows users to search for locations.

    Returns:
        A rendered template of the location page.
    """
    form = fo.LocationForm()
    return render_template('location.html', title='Location', form=form)

@current_app.route('/api/states/<country_name>')
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

@current_app.route('/api/cities/<country_name>/<int:state_id>')
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

@current_app.route('/api/location/<int:city_id>')
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

@current_app.route('/api/class_batches/<int:class_name_id>')
@login_required
def api_class_batches(class_name_id):
    """
    API endpoint to get class batches for a given class name ID.

    Args:
        class_name_id (int): The ID of the class name.

    Returns:
        A JSON response containing a list of class batches, each with an 'id'
        and 'name'.
    """
    batches = db.session.scalars(sa.select(ClassBatch).where(ClassBatch.class_name_id == class_name_id)).all()
    return jsonify([{'id': batch.id, 'name': batch.batch_no} for batch in batches])

@current_app.route('/api/class_regions/<int:class_batch_id>')
@login_required
def api_class_regions(class_batch_id):
    """Provides a list of class regions for a given class batch."""
    regions = db.session.scalars(sa.select(ClassRegion).where(ClassRegion.class_batch_id == class_batch_id)).all()
    return jsonify([{'id': region.id, 'name': region.section} for region in regions])

@current_app.route('/dashboard')
@login_required
def dashboard():
    """Renders the dashboard page."""
    num_students = db.session.query(mo.User).count()
    num_teachers = db.session.query(mo.ClassBatchTeacher).distinct(mo.ClassBatchTeacher.user_id).count()
    num_classes = db.session.query(mo.ClassName).count()
    num_batches = db.session.query(mo.ClassBatch).count()

    # Data for charts
    student_status_data = db.session.query(mo.UserStatus.status, sa.func.count(mo.StudentGroup.id)).join(mo.StudentGroup).group_by(mo.UserStatus.status).all()
    student_batch_data = db.session.query(mo.ClassBatch.batch_no, sa.func.count(mo.StudentGroup.id)).join(mo.ClassGroup).join(mo.StudentGroup).join(mo.ClassRegion).join(mo.ClassBatch).group_by(mo.ClassBatch.batch_no).all()

    chart_data = {
        'student_status': {
            'labels': [status[0] for status in student_status_data],
            'data': [status[1] for status in student_status_data]
        },
        'student_batch': {
            'labels': [batch[0] for batch in student_batch_data],
            'data': [batch[1] for batch in student_batch_data]
        }
    }

    return render_template('dashboard.html', title='Dashboard',
                           num_students=num_students,
                           num_teachers=num_teachers,
                           num_classes=num_classes,
                           num_batches=num_batches,
                           chart_data=chart_data)

@current_app.route('/calendar')
@login_required
def calendar():
    """Renders the calendar page."""
    events = []
    class_batches = db.session.query(mo.ClassBatch).all()
    for batch in class_batches:
        events.append({
            'title': f'{batch.class_name.name} - {batch.batch_no}',
            'start': batch.start_date.strftime('%Y-%m-%d'),
        })
    return render_template('calendar.html', title='Calendar', events=events)

@current_app.route('/messages')
@login_required
def messages():
    """Renders the messages page."""
    messages = db.session.query(mo.Message).filter(
        (mo.Message.sender_id == current_user.id) | (mo.Message.recipient_id == current_user.id)
    ).order_by(mo.Message.timestamp.desc()).all()
    return render_template('messages.html', title='Messages', messages=messages)

@current_app.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    """Renders the send_message page."""
    form = fo.MessageForm()
    if form.validate_on_submit():
        recipient = db.session.scalar(sa.select(mo.User).where(mo.User.username == form.recipient.data))
        if recipient:
            message = mo.Message(sender_id=current_user.id, recipient_id=recipient.id, body=form.body.data)
            db.session.add(message)
            db.session.commit()
            flash('Your message has been sent.')
            return redirect(url_for('messages'))
        else:
            flash('User not found.')
    return render_template('send_message.html', title='Send Message', form=form)

@current_app.route('/files')
@login_required
def files():
    """Renders the files page."""
    files = db.session.query(mo.File).filter(mo.File.user_id == current_user.id).all()
    return render_template('files.html', title='Files', files=files)

@current_app.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    """Renders the upload_file page."""
    form = fo.FileUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        new_file = mo.File(filename=file.filename, data=file.read(), user_id=current_user.id, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(new_file)
        db.session.commit()
        flash('Your file has been uploaded.')
        return redirect(url_for('files'))
    return render_template('upload_file.html', title='Upload File', form=form)

@current_app.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    """Downloads a file."""
    file = db.session.get(mo.File, file_id)
    if file and file.user_id == current_user.id:
        return send_file(BytesIO(file.data), download_name=file.filename, as_attachment=True)
    else:
        flash('File not found or you do not have permission to access it.')
        return redirect(url_for('files'))


@current_app.route('/class_name', methods=['GET', 'POST'])
@login_required
def class_name():
    form = ClassNameForm()
    if form.validate_on_submit():
        class_name = ClassName(name=form.name.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_name)
        db.session.commit()
        flash('Class name added successfully!')
        return redirect(url_for('class_name'))
    query = ClassName.query
    search = request.args.get('search')
    date_filter = request.args.get('date_filter')
    if search:
        query = query.filter(ClassName.name.like(f'%{search}%'))
    if date_filter:
        query = query.filter(sa.func.date(ClassName.created_at) == date_filter)
    classes = query.all()
    return render_template('class_name.html', title='Class Name', form=form, classes=classes)

@current_app.route('/class_batch', methods=['GET', 'POST'])
@login_required
def class_batch():
    """Renders the class batch page and handles the creation of new class batches."""
    form = ClassBatchForm()
    if form.validate_on_submit():
        try:
            class_batch = ClassBatch(class_name_id=form.class_name_id.data, batch_no=form.batch_no.data, start_date=form.start_date.data, status_id=form.status_id.data, created_by=current_user.id, updated_by=current_user.id)
            db.session.add(class_batch)
            db.session.commit()
            flash('Class batch added successfully!')
            return redirect(url_for('class_batch'))
        except sa.exc.IntegrityError:
            db.session.rollback()
            flash('A batch in the selected Class Name already exist', 'danger')
    query = ClassBatch.query
    search = request.args.get('search')
    if search:
        query = query.filter(ClassBatch.batch_no.like(f'%{search}%'))
    batches = query.all()
    return render_template('class_batch.html', title='Class Batch', form=form, batches=batches)

@current_app.route('/class_region', methods=['GET', 'POST'])
@login_required
def class_region():
    """
    Renders the class region page and handles the creation of new class regions.

    On GET request, it displays a form to create a new class region and a list
    of existing regions.
    On POST request, it validates the form data, creates a new ClassRegion object,
    and saves it to the database.
    """
    form = ClassRegionForm()
    if request.method == 'POST':
        class_name_id = request.form.get('class_name_id')
        if class_name_id:
            form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=class_name_id).all()]

    if form.validate_on_submit():
        class_region = ClassRegion(class_name_id=form.class_name_id.data, class_batch_id=form.class_batch_id.data, section=form.section.data, description=form.description.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_region)
        db.session.commit()
        flash('Class region added successfully!')
        return redirect(url_for('class_region'))
    query = ClassRegion.query
    search = request.args.get('search')
    if search:
        query = query.filter(ClassRegion.section.like(f'%{search}%'))
    regions = query.all()
    return render_template('class_region.html', title='Class Region', form=form, regions=regions)

@current_app.route('/class_group', methods=['GET', 'POST'])
@login_required
def class_group():
    form = ClassGroupForm()
    if request.method == 'POST':
        class_name_id = request.form.get('class_name_id')
        class_batch_id = request.form.get('class_batch_id')
        if class_name_id:
            form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=class_name_id).all()]
        if class_batch_id:
            form.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.filter_by(class_batch_id=class_batch_id).all()]

    if form.validate_on_submit():
        class_group = ClassGroup(name=form.name.data, class_region_id=form.class_region_id.data, description=form.description.data, start_index=form.start_index.data, end_index=form.end_index.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_group)
        db.session.commit()
        flash('Class group added successfully!')
        return redirect(url_for('class_group'))
    query = ClassGroup.query
    search = request.args.get('search')
    if search:
        query = query.filter(ClassGroup.description.like(f'%{search}%'))
    indexes = query.all()
    return render_template('class_group.html', title='Class Group', form=form, indexes=indexes)

@current_app.route('/class_group_mentor', methods=['GET', 'POST'])
@login_required
def class_group_mentor():
    """Renders the class group mentor page."""
    form = ClassGroupMentorForm()
    if form.validate_on_submit():
        class_group_mentor = ClassGroupMentor(user_id=form.user_id.data, class_name_id=form.class_name_id.data, class_batch_id=form.class_batch_id.data, class_region_id=form.class_region_id.data, class_group_id=form.class_group_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_group_mentor)
        db.session.commit()
        flash('Class group mentor added successfully!')
        return redirect(url_for('class_group_mentor'))
    mentors = ClassGroupMentor.query.all()
    return render_template('class_group_mentor.html', title='Class Group Mentor', form=form, mentors=mentors)

@current_app.route('/list_class_group_mentors')
@login_required
def list_class_group_mentors():
    """Renders the list_class_group_mentors page."""
    mentors = ClassGroupMentor.query.all()
    return render_template('list_class_group_mentors.html', title='List Class Group Mentors', mentors=mentors)


@current_app.route('/remove_class_group_mentor', methods=['GET', 'POST'])
@login_required
def remove_class_group_mentor():
    """Renders the remove_class_group_mentor page."""
    if request.method == 'POST':
        mentor_ids = request.form.getlist('mentor_ids')
        if mentor_ids:
            for mentor_id in mentor_ids:
                mentor_to_delete = ClassGroupMentor.query.get(mentor_id)
                db.session.delete(mentor_to_delete)
            db.session.commit()
            flash('Class group mentors deleted successfully!', 'success')
        return redirect(url_for('remove_class_group_mentor'))
    
    mentors = ClassGroupMentor.query.all()
    return render_template('remove_class_group_mentor.html', title='Remove Class Group Mentor', mentors=mentors)


@current_app.route('/update_class_group_mentor', methods=['GET'])
@login_required
def update_class_group_mentor():
    """Renders the update_class_group_mentor page."""
    mentors = ClassGroupMentor.query.all()
    return render_template('update_class_group_mentor.html', title='Update Class Group Mentor', mentors=mentors)


@current_app.route('/update_class_group_mentor/<int:id>', methods=['GET', 'POST'])
@login_required
def update_class_group_mentor_item(id):
    """Renders the update_class_group_mentor_item page."""
    mentor = ClassGroupMentor.query.get_or_404(id)
    form = ClassGroupMentorForm(obj=mentor)
    if form.validate_on_submit():
        mentor.user_id = form.user_id.data
        mentor.class_name_id = form.class_name_id.data
        mentor.class_batch_id = form.class_batch_id.data
        mentor.class_region_id = form.class_region_id.data
        mentor.class_group_id = form.class_group_id.data
        mentor.updated_by = current_user.id
        db.session.commit()
        flash('Class group mentor updated successfully!', 'success')
        return redirect(url_for('update_class_group_mentor'))
    return render_template('update_class_group_mentor_item.html', title='Update Class Group Mentor', form=form, mentor=mentor)


@current_app.route('/search_class_group_mentor', methods=['GET', 'POST'])
@login_required
def search_class_group_mentor():
    """Renders the search_class_group_mentor page."""
    form = ClassGroupMentorForm()
    mentors = []
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        if search_term:
            search_pattern = f'%{search_term}%'
            mentors = db.session.query(ClassGroupMentor).join(mo.User).join(mo.ClassName).join(mo.ClassBatch).outerjoin(mo.ClassRegion).outerjoin(mo.ClassGroup).filter(
                sa.or_(
                    mo.User.username.ilike(search_pattern),
                    mo.ClassName.name.ilike(search_pattern),
                    mo.ClassBatch.batch_no.ilike(search_pattern),
                    mo.ClassRegion.section.ilike(search_pattern) if mo.ClassRegion.section is not None else False,
                    mo.ClassGroup.description.ilike(search_pattern) if mo.ClassGroup.description is not None else False
                )
            ).all()
        else:
            flash('Please enter a search term.', 'warning')
    return render_template('search_class_group_mentor.html', title='Search Class Group Mentor', form=form, mentors=mentors)

@current_app.route('/user_status', methods=['GET', 'POST'])
@login_required
def user_status():
    """Renders the user_status page and handles the creation of new user statuses."""
    form = UserStatusForm()
    if form.validate_on_submit():
        user_status = UserStatusLookup(status=form.status.data, description=form.description.data)
        db.session.add(user_status)
        db.session.commit()
        flash('User status added successfully!')
        return redirect(url_for('user_status'))
    statuses = UserStatusLookup.query.all()
    return render_template('user_status.html', title='User Status', form=form, statuses=statuses)

@current_app.route('/list_user_statuses')
@login_required
def list_user_statuses():
    """Renders the list_user_statuses page."""
    statuses = UserStatusLookup.query.all()
    return render_template('list_user_statuses.html', title='List User Statuses', statuses=statuses)


@current_app.route('/remove_user_status', methods=['GET', 'POST'])
@login_required
def remove_user_status():
    """Renders the remove_user_status page."""
    if request.method == 'POST':
        status_ids = request.form.getlist('status_ids')
        if status_ids:
            for status_id in status_ids:
                status_to_delete = UserStatus.query.get(status_id)
                db.session.delete(status_to_delete)
            db.session.commit()
            flash('User statuses deleted successfully!', 'success')
        return redirect(url_for('remove_user_status'))
    
    statuses = UserStatus.query.all()
    return render_template('remove_user_status.html', title='Remove User Status', statuses=statuses)


@current_app.route('/update_user_status', methods=['GET'])
@login_required
def update_user_status():
    """Renders the update_user_status page."""
    statuses = UserStatus.query.all()
    return render_template('update_user_status.html', title='Update User Status', statuses=statuses)


@current_app.route('/update_user_status/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_status_item(id):
    """Renders the update_user_status_item page."""
    status = UserStatus.query.get_or_404(id)
    form = UserStatusForm(obj=status)
    if form.validate_on_submit():
        status.status = form.status.data
        status.description = form.description.data
        db.session.commit()
        flash('User status updated successfully!', 'success')
        return redirect(url_for('update_user_status'))
    return render_template('update_user_status_item.html', title='Update User Status', form=form, status=status)


@current_app.route('/search_user_status', methods=['GET', 'POST'])
@login_required
def search_user_status():
    """Renders the search_user_status page."""
    form = UserStatusForm()
    statuses = []
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        if search_term:
            search_pattern = f'%{search_term}%'
            statuses = UserStatus.query.filter(
                sa.or_(
                    UserStatus.status.ilike(search_pattern),
                    UserStatus.description.ilike(search_pattern)
                )
            ).all()
        else:
            flash('Please enter a search term.', 'warning')
    return render_template('search_user_status.html', title='Search User Status', form=form, statuses=statuses)

@current_app.route('/student_group', methods=['GET', 'POST'])
@login_required
def student_group():
    form = StudentGroupForm()
    if form.validate_on_submit():
        student_group = StudentGroup(user_id=form.user_id.data, class_group_id=form.class_group_id.data, index_no=form.index_no.data, status_id=form.status_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(student_group)
        db.session.commit()
        flash('Student group added successfully!')
        return redirect(url_for('student_group'))
    groups = StudentGroup.query.all()
    return render_template('student_group.html', title='Student Group', form=form, groups=groups)

@current_app.route('/class_batch_teacher', methods=['GET', 'POST'])
@login_required
def class_batch_teacher():
    """Renders the class_batch_teacher page and handles the creation of new class batch teachers."""
    form = ClassBatchTeacherForm()
    if form.validate_on_submit():
        class_batch_teacher = ClassBatchTeacher(user_id=form.user_id.data, class_batch_id=form.class_batch_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_batch_teacher)
        db.session.commit()
        flash('Class batch teacher added successfully!')
        return redirect(url_for('class_batch_teacher'))
    teachers = ClassBatchTeacher.query.all()
    return render_template('class_batch_teacher.html', title='Class Batch Teacher', form=form, teachers=teachers)

@current_app.route('/role', methods=['GET', 'POST'])
@login_required
def role():
    """Renders the role page and handles the creation of new roles."""
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(role=form.role.data, level=form.level.data, description=form.description.data)
        db.session.add(role)
        db.session.commit()
        flash('Role added successfully!')
        return redirect(url_for('role'))
    roles = Role.query.order_by(Role.level).all()
    return render_template('role.html', title='Role', form=form, roles=roles)

@current_app.route('/remove_role', methods=['GET', 'POST'])
@login_required
def remove_role():
    """Renders the remove_role page and handles the deletion of roles."""
    if request.method == 'POST':
        role_ids = request.form.getlist('role_ids')
        if role_ids:
            for role_id in role_ids:
                role_to_delete = Role.query.get(role_id)
                db.session.delete(role_to_delete)
            db.session.commit()
            flash('Roles deleted successfully!', 'success')
        return redirect(url_for('remove_role'))
    
    roles = Role.query.order_by(Role.level).all()
    return render_template('remove_role.html', title='Remove Role', roles=roles)

@current_app.route('/update_role', methods=['GET'])
@login_required
def update_role():
    """Renders the update_role page."""
    roles = Role.query.order_by(Role.level).all()
    return render_template('update_role.html', title='Update Role', roles=roles)

@current_app.route('/update_role/<int:id>', methods=['GET', 'POST'])
@login_required
def update_role_item(id):
    """Renders the update_role_item page and handles the update of a specific role."""
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.role = form.role.data
        role.level = form.level.data
        role.description = form.description.data
        db.session.commit()
        flash('Role updated successfully!', 'success')
        return redirect(url_for('update_role'))
    return render_template('update_role_item.html', title='Update Role', form=form, role=role)

@current_app.route('/list_roles')
@login_required
def list_roles():
    """Renders the list_roles page."""
    roles = Role.query.order_by(Role.level).all()
    return render_template('list_roles.html', title='List Roles', roles=roles)


@current_app.route('/remove_user_role', methods=['GET', 'POST'])
@login_required
def remove_user_role():
    form = fo.EmptyForm()
    if request.method == 'POST':
        user_role_ids = request.form.getlist('user_role_ids')
        if user_role_ids:
            for user_role_id in user_role_ids:
                user_role_to_delete = UserRole.query.get(user_role_id)
                db.session.delete(user_role_to_delete)
            db.session.commit()
            flash('User roles deleted successfully!', 'success')
        return redirect(url_for('remove_user_role'))
    
    user_roles = UserRole.query.all()
    return render_template('remove_user_role.html', title='Remove User Role', user_roles=user_roles, form=form)


@current_app.route('/update_user_role', methods=['GET'])
@login_required
def update_user_role():
    """Renders the update_user_role page."""
    query = UserRole.query
    search = request.args.get('search')
    if search:
        query = query.join(mo.User, mo.User.id == mo.UserRole.user_id).join(mo.Role).join(mo.ClassBatch).outerjoin(mo.ClassRegion).filter(
            sa.or_(
                mo.User.username.ilike(f'%{search}%'),
                mo.Role.role.ilike(f'%{search}%'),
                mo.ClassBatch.batch_no.ilike(f'%{search}%'),
                mo.ClassRegion.section.ilike(f'%{search}%')
            )
        )
    user_roles = query.all()
    return render_template('update_user_role.html', title='Update User Role', user_roles=user_roles)


@current_app.route('/update_user_role/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_role_item(id):
    user_role = UserRole.query.get_or_404(id)
    form = UserRoleForm(obj=user_role)

    # Populate class_name_id choices (always static)
    form.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]

    # Determine current class_name_id, class_batch_id, class_region_id
    # On POST, use submitted form data. On GET, use existing user_role data.
    current_class_name_id = None
    current_class_batch_id = None
    current_class_region_id = None

    if request.method == 'POST':
        current_class_name_id = request.form.get('class_name_id', type=int)
        current_class_batch_id = request.form.get('class_batch_id', type=int)
        class_region_id_str = request.form.get('class_region_id')
        current_class_region_id = int(class_region_id_str) if class_region_id_str and class_region_id_str != 'None' else None
    else: # GET request
        if user_role.class_batch:
            current_class_name_id = user_role.class_batch.class_name_id
        current_class_batch_id = user_role.class_batch_id
        current_class_region_id = user_role.class_region_id

    # Populate class_batch_id choices based on current_class_name_id
    if current_class_name_id:
        form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=current_class_name_id).all()]
    else:
        form.class_batch_id.choices = []

    # Populate class_region_id choices based on current_class_batch_id
    form.class_region_id.choices = [(None, 'All Regions')] # Always include 'All Regions'
    if current_class_batch_id:
        form.class_region_id.choices.extend([(r.id, r.section) for r in ClassRegion.query.filter_by(class_batch_id=current_class_batch_id).all()])
    
    # Populate class_group_id choices based on current_class_region_id
    if current_class_region_id is not None: # Only filter if a specific region is selected (not 'All Regions')
        form.class_group_id.choices = [(g.id, g.description) for g in ClassGroup.query.filter_by(class_region_id=current_class_region_id).all()]
        # If there are no groups for the selected region, still allow None
        if not form.class_group_id.choices:
            form.class_group_id.choices.insert(0, (None, ''))
    else:
        # If 'All Regions' is selected, allow None as a valid choice for Class Group
        form.class_group_id.choices = [(None, '')] # Allow empty selection for Class Group

    if form.validate_on_submit():
        user_role.user_id = form.user_id.data
        user_role.role_id = form.role_id.data
        user_role.class_batch_id = form.class_batch_id.data
        user_role.class_region_id = form.class_region_id.data # This will be None if 'All Regions' was selected
        user_role.class_group_id = form.class_group_id.data
        user_role.updated_by = current_user.id
        db.session.commit()
        flash('User role updated successfully!', 'success')
        return redirect(url_for('update_user_role'))
    elif request.method == 'POST': # Form did not validate on POST
        flash('Please correct the errors below.', 'danger')
        # The choices are already populated above, so no need to re-populate here.

    return render_template('update_user_role_item.html', title='Update User Role', form=form, user_role=user_role)


@current_app.route('/list_user_roles')
@login_required
def list_user_roles():
    """Renders the list_user_roles page."""
    query = UserRole.query
    search = request.args.get('search')
    if search:
        query = query.join(mo.User, mo.User.id == mo.UserRole.user_id).join(mo.Role).join(mo.ClassBatch).outerjoin(mo.ClassRegion).filter(
            sa.or_(
                mo.User.username.ilike(f'%{search}%'),
                mo.Role.role.ilike(f'%{search}%'),
                mo.ClassBatch.batch_no.ilike(f'%{search}%'),
                mo.ClassRegion.section.ilike(f'%{search}%')
            )
        )
    user_roles = query.all()
    return render_template('list_user_roles.html', title='List User Roles', user_roles=user_roles)


@current_app.route('/user_role', methods=['GET', 'POST'])
@login_required
def user_role():
    form = UserRoleForm()
    if request.method == 'POST':
        class_name_id = request.form.get('class_name_id')
        class_batch_id = request.form.get('class_batch_id')

        if class_name_id:
            form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=class_name_id).all()]
        else:
            form.class_batch_id.choices = []

        if class_batch_id:
            form.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.filter_by(class_batch_id=class_batch_id).all()]
        else:
            form.class_region_id.choices = []

    if form.validate_on_submit():
        try:
            user_id = form.user_id.data
            role_id = form.role_id.data
            class_batch_id = form.class_batch_id.data

            user_role = UserRole(user_id=user_id, role_id=role_id, class_batch_id=class_batch_id, created_by=current_user.id, updated_by=current_user.id)
            db.session.add(user_role)
            db.session.commit()
            flash('User role added successfully!')
            return redirect(url_for('user_role'))
        except sa.exc.IntegrityError:
            db.session.rollback()
            flash('This user role already exists.', 'danger')
        
    user_roles = UserRole.query.all()
    return render_template('user_role.html', title='User Role', form=form, user_roles=user_roles)

@current_app.route('/user/<username>')
@login_required
def user_profile(username):
    """Renders the user profile page."""
    user = db.session.scalar(sa.select(mo.User).where(mo.User.username == username))
    if not user:
        flash('User not found.')
        return redirect(url_for('index'))
    
    student_groups = db.session.query(mo.StudentGroup).filter_by(user_id=user.id).all()
    
    return render_template('user_profile.html', title='User Profile', user=user, student_groups=student_groups)


@current_app.route('/class_batch_status', methods=['GET', 'POST'])
@login_required
def class_batch_status():
    form = ClassBatchStatusForm()
    if form.validate_on_submit():
        class_batch_status = ClassBatchStatus(status=form.status.data)
        db.session.add(class_batch_status)
        db.session.commit()
        flash('Class batch status added successfully!')
        return redirect(url_for('class_batch_status'))
    statuses = ClassBatchStatus.query.all()
    return render_template('class_batch_status.html', title='Class Batch Status', form=form, statuses=statuses)


@current_app.route('/list_class_names')
@login_required
def list_class_names():
    """Renders the list_class_names page."""
    class_names = ClassName.query.all()
    return render_template('list_class_names.html', title='List Class Names', class_names=class_names)


@current_app.route('/search_class_name', methods=['GET', 'POST'])
@login_required
def search_class_name():
    """Renders the search_class_name page."""
    form = ClassNameForm()
    class_names = []
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        if search_term and len(search_term) >= 3:
            class_names = ClassName.query.filter(ClassName.name.ilike(f'%{search_term}%')).all()
        else:
            flash('Please enter at least 3 characters to search.', 'warning')
    return render_template('search_class_name.html', title='Search Class Name', form=form, class_names=class_names)


@current_app.route('/remove_class_name', methods=['GET', 'POST'])
@login_required
def remove_class_name():
    """Renders the remove_class_name page."""
    if request.method == 'POST':
        class_ids = request.form.getlist('class_ids')
        if class_ids:
            for class_id in class_ids:
                class_to_delete = ClassName.query.get(class_id)
                db.session.delete(class_to_delete)
            db.session.commit()
            flash('Class names deleted successfully!', 'success')
        return redirect(url_for('remove_class_name'))
    
    class_names = ClassName.query.all()
    return render_template('remove_class_name.html', title='Remove Class Name', class_names=class_names)


@current_app.route('/update_class_name', methods=['GET'])
@login_required
def update_class_name():
    """Renders the update_class_name page."""
    class_names = ClassName.query.all()
    return render_template('update_class_name.html', title='Update Class Name', class_names=class_names)


@current_app.route('/update_class_name/<int:id>', methods=['GET', 'POST'])
@login_required
def update_class_name_item(id):
    """Renders the update_class_name_item page."""
    class_name = ClassName.query.get_or_404(id)
    form = ClassNameForm(obj=class_name)
    if form.validate_on_submit():
        class_name.name = form.name.data
        class_name.updated_by = current_user.id
        db.session.commit()
        flash('Class name updated successfully!', 'success')
        return redirect(url_for('update_class_name'))
    return render_template('update_class_name_item.html', title='Update Class Name', form=form, class_name=class_name)


@current_app.route('/list_class_batch_statuses')
@login_required
def list_class_batch_statuses():
    """Renders the list_class_batch_statuses page."""
    statuses = ClassBatchStatus.query.all()
    return render_template('list_class_batch_statuses.html', title='List Class Batch Statuses', statuses=statuses)


@current_app.route('/remove_class_batch_status', methods=['GET', 'POST'])
@login_required
def remove_class_batch_status():
    """Renders the remove_class_batch_status page."""
    if request.method == 'POST':
        status_ids = request.form.getlist('status_ids')
        if status_ids:
            for status_id in status_ids:
                status_to_delete = ClassBatchStatus.query.get(status_id)
                db.session.delete(status_to_delete)
            db.session.commit()
            flash('Class batch statuses deleted successfully!', 'success')
        return redirect(url_for('remove_class_batch_status'))
    
    statuses = ClassBatchStatus.query.all()
    return render_template('remove_class_batch_status.html', title='Remove Class Batch Status', statuses=statuses)


@current_app.route('/update_class_batch_status', methods=['GET'])
@login_required
def update_class_batch_status():
    """Renders the update_class_batch_status page."""
    statuses = ClassBatchStatus.query.all()
    return render_template('update_class_batch_status.html', title='Update Class Batch Status', statuses=statuses)


@current_app.route('/update_class_batch_status/<int:id>', methods=['GET', 'POST'])
@login_required
def update_class_batch_status_item(id):
    """Renders the update_class_batch_status_item page."""
    status = ClassBatchStatus.query.get_or_404(id)
    form = ClassBatchStatusForm(obj=status)
    if form.validate_on_submit():
        status.status = form.status.data
        db.session.commit()
        flash('Class batch status updated successfully!', 'success')
        return redirect(url_for('update_class_batch_status'))
    return render_template('update_class_batch_status_item.html', title='Update Class Batch Status', form=form, status=status)


@current_app.route('/list_class_batches')
@login_required
def list_class_batches():
    """Renders the list_class_batches page."""
    batches = ClassBatch.query.all()
    return render_template('list_class_batches.html', title='List Class Batches', batches=batches)


@current_app.route('/remove_class_batch', methods=['GET', 'POST'])
@login_required
def remove_class_batch():
    """Renders the remove_class_batch page."""
    if request.method == 'POST':
        batch_ids = request.form.getlist('batch_ids')
        if batch_ids:
            for batch_id in batch_ids:
                batch_to_delete = ClassBatch.query.get(batch_id)
                db.session.delete(batch_to_delete)
            db.session.commit()
            flash('Class batches deleted successfully!', 'success')
        return redirect(url_for('remove_class_batch'))
    
    batches = ClassBatch.query.all()
    return render_template('remove_class_batch.html', title='Remove Class Batch', batches=batches)


@current_app.route('/update_class_batch', methods=['GET'])
@login_required
def update_class_batch():
    """Renders the update_class_batch page."""
    batches = ClassBatch.query.all()
    return render_template('update_class_batch.html', title='Update Class Batch', batches=batches)


@current_app.route('/update_class_batch/<int:id>', methods=['GET', 'POST'])
@login_required
def update_class_batch_item(id):
    """Renders the update_class_batch_item page."""
    batch = ClassBatch.query.get_or_404(id)
    form = ClassBatchForm(obj=batch)
    if form.validate_on_submit():
        batch.class_name_id = form.class_name_id.data
        batch.batch_no = form.batch_no.data
        batch.start_date = form.start_date.data
        batch.status_id = form.status_id.data
        batch.updated_by = current_user.id
        db.session.commit()
        flash('Class batch updated successfully!', 'success')
        return redirect(url_for('update_class_batch'))
    return render_template('update_class_batch_item.html', title='Update Class Batch', form=form, batch=batch)


@current_app.route('/list_class_regions')
@login_required
def list_class_regions():
    """Renders the list_class_regions page."""
    regions = ClassRegion.query.all()
    return render_template('list_class_regions.html', title='List Class Regions', regions=regions)


@current_app.route('/remove_class_region', methods=['GET', 'POST'])
@login_required
def remove_class_region():
    """Renders the remove_class_region page."""
    if request.method == 'POST':
        region_ids = request.form.getlist('region_ids')
        if region_ids:
            for region_id in region_ids:
                region_to_delete = ClassRegion.query.get(region_id)
                db.session.delete(region_to_delete)
            db.session.commit()
            flash('Class regions deleted successfully!', 'success')
        return redirect(url_for('remove_class_region'))
    
    regions = ClassRegion.query.all()
    return render_template('remove_class_region.html', title='Remove Class Region', regions=regions)


@current_app.route('/update_class_region', methods=['GET'])
@login_required
def update_class_region():
    """Renders the update_class_region page."""
    regions = ClassRegion.query.all()
    return render_template('update_class_region.html', title='Update Class Region', regions=regions)


@current_app.route('/update_class_region/<int:id>', methods=['GET', 'POST'])
@login_required
def update_class_region_item(id):
    """Renders the update_class_region_item page."""
    region = ClassRegion.query.get_or_404(id)
    form = ClassRegionForm(obj=region)
    form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=region.class_name_id).all()]

    if request.method == 'POST':
        class_name_id = request.form.get('class_name_id')
        if class_name_id:
            form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=class_name_id).all()]

    if form.validate_on_submit():
        region.class_name_id = form.class_name_id.data
        region.class_batch_id = form.class_batch_id.data
        region.section = form.section.data
        region.description = form.description.data
        region.updated_by = current_user.id
        db.session.commit()
        flash('Class region updated successfully!', 'success')
        return redirect(url_for('update_class_region'))
    return render_template('update_class_region_item.html', title='Update Class Region', form=form, region=region)


@current_app.route('/list_class_groups')
@login_required
def list_class_groups():
    """Renders the list_class_groups page."""
    indexes = ClassGroup.query.all()
    return render_template('list_class_groups.html', title='List Class Groupes', indexes=indexes)


@current_app.route('/remove_class_group', methods=['GET', 'POST'])
@login_required
def remove_class_group():
    """Renders the remove_class_group page."""
    if request.method == 'POST':
        index_ids = request.form.getlist('index_ids')
        if index_ids:
            for index_id in index_ids:
                index_to_delete = ClassGroup.query.get(index_id)
                db.session.delete(index_to_delete)
            db.session.commit()
            flash('Class Groupes deleted successfully!', 'success')
        return redirect(url_for('remove_class_group'))
    
    indexes = ClassGroup.query.all()
    return render_template('remove_class_group.html', title='Remove Class Group', indexes=indexes)


@current_app.route('/update_class_group', methods=['GET'])
@login_required
def update_class_group():
    """Renders the update_class_group page."""
    indexes = ClassGroup.query.all()
    return render_template('update_class_group.html', title='Update Class Group', indexes=indexes)


@current_app.route('/update_class_group/<int:id>', methods=['GET', 'POST'])
@login_required
def update_class_group_item(id):
    """Renders the update_class_group_item page."""
    index = ClassGroup.query.get_or_404(id)
    form = ClassGroupForm(obj=index)
    
    # Populate choices
    form.class_name_id.choices = [(c.id, c.name) for c in ClassName.query.all()]
    form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=index.class_region.class_name_id).all()]
    form.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.filter_by(class_batch_id=index.class_region.class_batch_id).all()]

    if request.method == 'POST':
        class_name_id = request.form.get('class_name_id')
        class_batch_id = request.form.get('class_batch_id')
        if class_name_id:
            form.class_batch_id.choices = [(b.id, b.batch_no) for b in ClassBatch.query.filter_by(class_name_id=class_name_id).all()]
        if class_batch_id:
            form.class_region_id.choices = [(r.id, r.section) for r in ClassRegion.query.filter_by(class_batch_id=class_batch_id).all()]

    if form.validate_on_submit():
        index.name = form.name.data
        index.class_region_id = form.class_region_id.data
        index.description = form.description.data
        index.start_index = form.start_index.data
        index.end_index = form.end_index.data
        index.updated_by = current_user.id
        db.session.commit()
        flash('Class group updated successfully!', 'success')
        return redirect(url_for('update_class_group'))
        
    # Pre-select values for GET request
    form.class_name_id.data = index.class_region.class_name_id
    form.class_batch_id.data = index.class_region.class_batch_id
    form.class_region_id.data = index.class_region_id

    return render_template('update_class_group_item.html', title='Update Class Group', form=form, group=index)


@current_app.route('/search_class_group', methods=['GET', 'POST'])
@login_required
def search_class_group():
    """Renders the search_class_group page."""
    form = fo.SearchClassGroupForm()
    groups = []
    if form.validate_on_submit():
        search_term = form.search.data
        search_pattern = f'%{search_term}%'
        groups = db.session.query(ClassGroup).filter(
            sa.or_(
                ClassGroup.name.ilike(search_pattern),
                ClassGroup.description.ilike(search_pattern)
            )
        ).all()
    return render_template('search_class_group.html', title='Search Class Group', form=form, groups=groups)


@current_app.route('/search_user_password', methods=['GET', 'POST'])
@login_required
def search_user_password():
    form = fo.SearchUserForm()
    users = []
    action = request.args.get('action', 'update')  # Default to 'update'

    if form.validate_on_submit():
        search_term = form.search.data
        users = db.session.query(mo.User).join(mo.User.contact).filter(
            sa.or_(
                mo.User.username.ilike(f'%{search_term}%'),
                mo.Contact.email.ilike(f'%{search_term}%')
            )
        ).all()
    return render_template('search_user_password.html', form=form, users=users, action=action)

@current_app.route('/update_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_password(user_id):
    """Handles the update password functionality for an admin user."""
    if not current_user.username == 'admin': # TODO: later add condition check role
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))
    
    user = db.session.get(mo.User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('search_user_password'))

    form = fo.AdminChangePasswordForm()
    if form.validate_on_submit():
        password = db.session.scalar(sa.select(mo.Password).where(mo.Password.user_id == user.id))
        if password:
            password.password_hash = generate_password_hash(form.password.data)
            password.is_allowed = form.is_allowed.data
            password.force_change = form.force_change.data
            db.session.commit()
            flash(f'Password for {user.username} has been updated.', 'success')
        else:
            new_password = mo.Password(user_id=user.id, 
                                     password_hash=generate_password_hash(form.password.data), 
                                     is_allowed=form.is_allowed.data, 
                                     force_change=form.force_change.data)
            db.session.add(new_password)
            db.session.commit()
            flash(f'Password for {user.username} has been set.', 'success')
        return redirect(url_for('search_user_password'))

    return render_template('update_password.html', form=form, user=user)

@current_app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Handles the change password functionality for the logged-in user."""
    form = fo.ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.password.check_password(form.current_password.data):
            current_user.password.set_password(form.new_password.data)
            current_user.password.force_change = False
            current_user.password.attempt_counts = 0
            db.session.commit()
            flash('Your password has been changed successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid current password.', 'danger')
    return render_template('change_password.html', form=form)

@current_app.route('/list_passwords')
@login_required
def list_passwords():
    """Renders the list_passwords page."""
    if not current_user.username == 'admin':
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))
    users = db.session.query(mo.User).all()
    return render_template('list_passwords.html', users=users)

@current_app.route('/remove_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def remove_password(user_id):
    """Handles the removal of a user's password."""
    if not current_user.username == 'admin': # TODO: later add condition check role
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))
    
    user = db.session.get(mo.User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('search_user_password'))

    if request.method == 'POST':
        password = db.session.scalar(sa.select(mo.Password).where(mo.Password.user_id == user.id))
        if password:
            db.session.delete(password)
            db.session.commit()
            flash(f'Password for {user.username} has been removed.', 'success')
        else:
            flash(f'Password for {user.username} not found.', 'danger')
        return redirect(url_for('search_user_password'))

    return render_template('remove_password.html', user=user)


@current_app.route('/remove_passwords', methods=['POST'])
@login_required
def remove_passwords():
    """Handles the removal of multiple user passwords."""
    if not current_user.username == 'admin': # TODO: later add condition check role
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('index'))
    
    user_ids = request.form.getlist('user_ids')
    if user_ids:
        for user_id in user_ids:
            password = db.session.scalar(sa.select(mo.Password).where(mo.Password.user_id == user_id))
            if password:
                db.session.delete(password)
        db.session.commit()
        flash(f'{len(user_ids)} password(s) have been removed.', 'success')
    else:
        flash('No users were selected.', 'warning')
    return redirect(url_for('search_user_password'))

@current_app.route('/search_referrer', methods=['GET', 'POST'])
@login_required
def search_referrer():
    form = ReferrerSearchForm()
    users = []
    if form.validate_on_submit():
        search_term = form.search.data
        users = db.session.query(mo.User).join(mo.User.contact).filter(
            sa.or_(
                mo.User.username.ilike(f'%{search_term}%'),
                mo.Contact.email.ilike(f'%{search_term}%'),
                mo.Contact.mobile.ilike(f'%{search_term}%')
            )
        ).all()
    return render_template('search_referrer_results.html', title='Search Referrer', form=form, users=users)


@current_app.route('/update_referrer/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_referrer(user_id):
    user = db.session.get(mo.User, user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('search_referrer'))
    referrer = db.session.scalar(sa.select(Referrer).where(Referrer.user_id == user_id))
    form = UpdateReferrerForm(obj=referrer)
    if form.validate_on_submit():
        profile_url = url_for('user_profile', username=user.username)
        if referrer:
            referrer.full_name = form.full_name.data
            referrer.mobile = form.mobile.data
            referrer.email = form.email.data
            referrer.batch = form.batch.data
            referrer.referrer_id = form.referrer_id.data
            flash(f'Referrer details for <a href="{profile_url}">{user.username}</a> updated.')
        else:
            referrer = Referrer(
                user_id=user_id,
                full_name=form.full_name.data,
                mobile=form.mobile.data,
                email=form.email.data,
                batch=form.batch.data,
                referrer_id=form.referrer_id.data
            )
            db.session.add(referrer)
            flash(f'Referrer details for <a href="{profile_url}">{user.username}</a> added.')
        db.session.commit()
        return redirect(url_for('search_referrer'))
    return render_template('update_referrer.html', title='Update Referrer', form=form, user=user)
