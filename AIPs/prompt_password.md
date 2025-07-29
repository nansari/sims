Website users are going to use his email (stored in Contact model)  and password_hash(stored in Password model) to login. 
An exising user admin whose user_id is 1 is able to login using noreply1@google.com	email.


Update route in routes.py, realted forms in forms.py and create or update tmplates/*.html to implement following:
- add Password submeuItems under Add, Remove, Update, List and Search Nav Menu
- We should be able to search user based on partial name or partial email address and select it to Remove, Update, List and Search Password of a user. In search results, display 
    - username, id from User model
    - email, whatsapp and mobile from Contact model
    - 10 character of password_hash, attempt_count, is_allowed, force_chage, last_attempt_time, last_successful_attempt_time from Password model
- only user admin or other user with Admin role (that is maintained in UserRole model)can change password of another user. If admins are changing password of other user, then set force_chage to True
- in Profile Nav Menu, add submenuItem "Change Password" that a user can use to change his own password. It should ask existing password once and new password twice. If correct exising password is provided, then update Password table with new password_hash, set attempt_count to 0 and force_chage to False
- if force_chage is set to True, redirect user to change his password.

List the plan before making the changes.