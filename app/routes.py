#
import json
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, send_file
from flask import jsonify
from io import BytesIO
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import ClassNameForm, ClassBatchForm, ClassRegionForm, ClassGroupIndexForm, ClassGroupMentorForm, UserStatusForm, StudentGroupForm, ClassBatchTeacherForm, RoleForm, UserRoleForm, ClassBatchStatusForm
from app.models import ClassName, ClassBatch, ClassRegion, ClassGroupIndex, ClassGroupMentor, UserStatus, StudentGroup, ClassBatchTeacher, Role, UserRole, ClassBatchStatus
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
            flash('Invalid email or password', 'danger')
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
                flash(f'Password for <a href="{url_for('user_profile', username=user.username)}">{user.id}</a> updated.')
            else:
                password = mo.Password(user_id=user.id, password_hash=generate_password_hash(form.password.data))
                db.session.add(password)
                flash(f'Password for <a href="{url_for('user_profile', username=user.username)}">{user.id}</a> added.')
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

@app.route('/dashboard')
@login_required
def dashboard():
    """Renders the dashboard page."""
    num_students = db.session.query(mo.User).count()
    num_teachers = db.session.query(mo.ClassBatchTeacher).distinct(mo.ClassBatchTeacher.user_id).count()
    num_classes = db.session.query(mo.ClassName).count()
    num_batches = db.session.query(mo.ClassBatch).count()

    # Data for charts
    student_status_data = db.session.query(mo.UserStatus.status, sa.func.count(mo.StudentGroup.id)).join(mo.StudentGroup).group_by(mo.UserStatus.status).all()
    student_batch_data = db.session.query(mo.ClassBatch.batch_no, sa.func.count(mo.StudentGroup.id)).join(mo.ClassGroupIndex).join(mo.StudentGroup).join(mo.ClassRegion).join(mo.ClassBatch).group_by(mo.ClassBatch.batch_no).all()

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

@app.route('/calendar')
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

@app.route('/messages')
@login_required
def messages():
    """Renders the messages page."""
    messages = db.session.query(mo.Message).filter(
        (mo.Message.sender_id == current_user.id) | (mo.Message.recipient_id == current_user.id)
    ).order_by(mo.Message.timestamp.desc()).all()
    return render_template('messages.html', title='Messages', messages=messages)

@app.route('/send_message', methods=['GET', 'POST'])
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

@app.route('/files')
@login_required
def files():
    """Renders the files page."""
    files = db.session.query(mo.File).filter(mo.File.user_id == current_user.id).all()
    return render_template('files.html', title='Files', files=files)

@app.route('/upload_file', methods=['GET', 'POST'])
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

@app.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    """Downloads a file."""
    file = db.session.get(mo.File, file_id)
    if file and file.user_id == current_user.id:
        return send_file(BytesIO(file.data), download_name=file.filename, as_attachment=True)
    else:
        flash('File not found or you do not have permission to access it.')
        return redirect(url_for('files'))


@app.route('/class_name', methods=['GET', 'POST'])
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

@app.route('/class_batch', methods=['GET', 'POST'])
@login_required
def class_batch():
    form = ClassBatchForm()
    if form.validate_on_submit():
        class_batch = ClassBatch(class_name_id=form.class_name_id.data, batch_no=form.batch_no.data, start_date=form.start_date.data, status_id=form.status_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_batch)
        db.session.commit()
        flash('Class batch added successfully!')
        return redirect(url_for('class_batch'))
    query = ClassBatch.query
    search = request.args.get('search')
    if search:
        query = query.filter(ClassBatch.batch_no.like(f'%{search}%'))
    batches = query.all()
    return render_template('class_batch.html', title='Class Batch', form=form, batches=batches)

@app.route('/class_region', methods=['GET', 'POST'])
@login_required
def class_region():
    form = ClassRegionForm()
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

@app.route('/class_group_index', methods=['GET', 'POST'])
@login_required
def class_group_index():
    form = ClassGroupIndexForm()
    if form.validate_on_submit():
        class_group_index = ClassGroupIndex(class_region_id=form.class_region_id.data, description=form.description.data, start_index=form.start_index.data, end_index=form.end_index.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_group_index)
        db.session.commit()
        flash('Class group index added successfully!')
        return redirect(url_for('class_group_index'))
    query = ClassGroupIndex.query
    search = request.args.get('search')
    if search:
        query = query.filter(ClassGroupIndex.description.like(f'%{search}%'))
    indexes = query.all()
    return render_template('class_group_index.html', title='Class Group Index', form=form, indexes=indexes)

@app.route('/class_group_mentor', methods=['GET', 'POST'])
@login_required
def class_group_mentor():
    form = ClassGroupMentorForm()
    if form.validate_on_submit():
        class_group_mentor = ClassGroupMentor(user_id=form.user_id.data, class_name_id=form.class_name_id.data, class_batch_id=form.class_batch_id.data, class_region_id=form.class_region_id.data, class_group_id=form.class_group_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_group_mentor)
        db.session.commit()
        flash('Class group mentor added successfully!')
        return redirect(url_for('class_group_mentor'))
    mentors = ClassGroupMentor.query.all()
    return render_template('class_group_mentor.html', title='Class Group Mentor', form=form, mentors=mentors)

@app.route('/user_status', methods=['GET', 'POST'])
@login_required
def user_status():
    form = UserStatusForm()
    if form.validate_on_submit():
        user_status = UserStatus(status=form.status.data, description=form.description.data)
        db.session.add(user_status)
        db.session.commit()
        flash('User status added successfully!')
        return redirect(url_for('user_status'))
    statuses = UserStatus.query.all()
    return render_template('user_status.html', title='User Status', form=form, statuses=statuses)

@app.route('/student_group', methods=['GET', 'POST'])
@login_required
def student_group():
    form = StudentGroupForm()
    if form.validate_on_submit():
        student_group = StudentGroup(student_id=form.student_id.data, class_group_id=form.class_group_id.data, index_no=form.index_no.data, status_id=form.status_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(student_group)
        db.session.commit()
        flash('Student group added successfully!')
        return redirect(url_for('student_group'))
    groups = StudentGroup.query.all()
    return render_template('student_group.html', title='Student Group', form=form, groups=groups)

@app.route('/class_batch_teacher', methods=['GET', 'POST'])
@login_required
def class_batch_teacher():
    form = ClassBatchTeacherForm()
    if form.validate_on_submit():
        class_batch_teacher = ClassBatchTeacher(user_id=form.user_id.data, class_batch_id=form.class_batch_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(class_batch_teacher)
        db.session.commit()
        flash('Class batch teacher added successfully!')
        return redirect(url_for('class_batch_teacher'))
    teachers = ClassBatchTeacher.query.all()
    return render_template('class_batch_teacher.html', title='Class Batch Teacher', form=form, teachers=teachers)

@app.route('/role', methods=['GET', 'POST'])
@login_required
def role():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(role=form.role.data, level=form.level.data, description=form.description.data)
        db.session.add(role)
        db.session.commit()
        flash('Role added successfully!')
        return redirect(url_for('role'))
    roles = Role.query.all()
    return render_template('role.html', title='Role', form=form, roles=roles)

@app.route('/list_roles')
@login_required
def list_roles():
    """Renders the list_roles page."""
    roles = Role.query.all()
    return render_template('list_roles.html', title='List Roles', roles=roles)


@app.route('/user_role', methods=['GET', 'POST'])
@login_required
def user_role():
    form = UserRoleForm()
    if form.validate_on_submit():
        user_role = UserRole(user_id=form.user_id.data, role_id=form.role_id.data, class_region_id=form.class_region_id.data, class_batch_id=form.class_batch_id.data, class_group_id=form.class_group_id.data, created_by=current_user.id, updated_by=current_user.id)
        db.session.add(user_role)
        db.session.commit()
        flash('User role added successfully!')
        return redirect(url_for('user_role'))
    user_roles = UserRole.query.all()
    return render_template('user_role.html', title='User Role', form=form, user_roles=user_roles)

@app.route('/user/<username>')
@login_required
def user_profile(username):
    """Renders the user profile page."""
    user = db.session.scalar(sa.select(mo.User).where(mo.User.username == username))
    if not user:
        flash('User not found.')
        return redirect(url_for('index'))
    
    student_groups = db.session.query(mo.StudentGroup).filter_by(student_id=user.id).all()
    
    return render_template('user_profile.html', title='User Profile', user=user, student_groups=student_groups)


@app.route('/class_batch_status', methods=['GET', 'POST'])
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


@app.route('/list_class_names')
@login_required
def list_class_names():
    """Renders the list_class_names page."""
    class_names = ClassName.query.all()
    return render_template('list_class_names.html', title='List Class Names', class_names=class_names)


@app.route('/search_class_name', methods=['GET', 'POST'])
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


@app.route('/remove_class_name', methods=['GET', 'POST'])
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


@app.route('/update_class_name', methods=['GET'])
@login_required
def update_class_name():
    """Renders the update_class_name page."""
    class_names = ClassName.query.all()
    return render_template('update_class_name.html', title='Update Class Name', class_names=class_names)


@app.route('/update_class_name/<int:id>', methods=['GET', 'POST'])
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


@app.route('/list_class_batch_statuses')
@login_required
def list_class_batch_statuses():
    """Renders the list_class_batch_statuses page."""
    statuses = ClassBatchStatus.query.all()
    return render_template('list_class_batch_statuses.html', title='List Class Batch Statuses', statuses=statuses)


@app.route('/remove_class_batch_status', methods=['GET', 'POST'])
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


@app.route('/update_class_batch_status', methods=['GET'])
@login_required
def update_class_batch_status():
    """Renders the update_class_batch_status page."""
    statuses = ClassBatchStatus.query.all()
    return render_template('update_class_batch_status.html', title='Update Class Batch Status', statuses=statuses)


@app.route('/update_class_batch_status/<int:id>', methods=['GET', 'POST'])
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


