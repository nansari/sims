from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import logout_user

# import request
# import socket
# import secrets
# import logging
from . import forms

# from flask_debugtoolbar import DebugToolbarExtension

# @app.route('/home')
@app.route('/')
@app.route('/index')
def index():
    """Renders the home page."""
    user = {'username': 'Nasim'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    form = LoginForm()
    # always False for GET method
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/logout')
def logout():
    """Renders the logout page."""
    logout_user()
    return redirect(url_for('index'))

# @app.route('/')
# @app.route('/home')
# def index():
#     """Renders the home page."""
#     logging.warning("See this message in Flask Debug Toolbar!")
#     return render_template('index.html')

@app.route('/reg_template', methods=['GET', 'POST'])
def reg_template():
    # selected_batch = redirect(url_for('select_a_batch'))
    # print(selected_batch.data)
    form = forms.BatchForm()
    if request.method == 'POST':
        # render_template('select_batch.html', form=form)
        # selected_batch = form.batch.data
        select_a_batch = request.form.get('batch')
        return render_template('reg_template.html', batch=select_a_batch)

    return render_template('select_batch.html', form=form)


@app.route('/select_a_batch', methods=['GET', 'POST'])
def select_a_batch():

    form = forms.BatchForm()
    
    # # Fetch predefined batches from the database
    # form.batch.choices = [(batch.id, batch.name) for batch in Batch.query.all()]  # Adjust according to your model

    form = forms.BatchForm()
    if request.method == 'POST':
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
    if request.method == 'POST':
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

@app.route('/support', methods=['GET', 'POST'])
def support():
    """Renders the support page."""
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('support.html')

@app.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    form = forms.UserRegForm()
    if request.method == 'POST':
        # request.args is ImmutableMultiDict([]) 
        # request.form is :ImmutableMultiDict([('csrf_token', 'ac'), ('batch', 'KARAMA-08'), ('email', 'adsfa@sdfsd.com'), ('name', 'asdf'), ('gender', 'M'), ('yob', '1980'), ('mobile', '987979879'), ('hometowncity', '987979879'), ('hometowncity', '987979879'), ('hometowndistrict', 'sdf'), ('hometownstate', 'sdf'), ('hometowncountry', 'sdf'), ('residencecity', 'sdf'), ('residencestate', 'asdf'), ('residentcountry', 'sdf'), ('residentzip', '2343'), ('education', 'sdf'), ('profession', 'asdf'), ('referrer_id', '344'), ('status', 'CallOut'), ('bio', 'wqerwe'), ('submit', 'Submit')])
        flash("User is registered wioth data request.args {} request.form:{}".format( request.args, request.form))
    return render_template('user_reg.html', form=form)


@app.route('/show_a_user/<user_id>', methods=['GET', 'POST'])
def show_a_user(user_id):
    # return f"<html><body><p>Display user details of {user_id}</p></body></html>"
    return render_template('show_a_user.html', user_id=user_id)

def create_app():
    # app.debug = Config.DEBUG
    sk = Config.SECRET_KEY
    logging.warning("Debug Secret Key is: %s", sk)
    app.config['SECRET_KEY'] = sk
    toolbar = DebugToolbarExtension(app)
    return app
