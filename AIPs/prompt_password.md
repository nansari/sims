You are an expert web developer.
User is going to use his email address and password to login.

Update User Class:
- to read password_hash from Password table if user id is present in user_id colum of password table created by Password table . 

Update Password class:
- Password class will store hash password
- user_id must be uniq, no duplicate is allowed

Update route in routes.py and realted form in forms.py
- to Add password for a user who can be searched by using partial name, partial email or ID
- create templates\password.html
- create Password class in forms.py to render the form to serach the user from user table by partial name, partial email or ID. password should be typed twice to ensure integrity.
- If there is already user entry in Password table, on submission, flash message should tell that there was already password and it it is updated otherwise it should tell that new password is added.  Show hyperlink for the user ID that should show all user data from User table.

If database and User table is being create first time, add a admin user with admin123 password and admin@sims.com - all other user field use random values. create a script in data\initial_data\0_first_user.sql to create admin user later on.

Also create a script in data\wipe_database.py to clean up existing database in case I need to start afresh whenever it is needed.

You may implement additional related features if you can.

List the plan before making the changes.