
# TASKS TO IMPLEMENT
## Password Management related tools
- Add Password submeuItems under Add, Remove, Update, List and Search Nav Menu
- Create a '/app/templates/password_base.html' template that takes partial email address from Email table and to list all user ID, name, email address, country etc to select one of them
-  password_base.html templates can be extended in other new templates required to implement all other features
- Password submeuItems under Add Nav Menu, will ask new password for the user twice and if both both input are exactly same
    - it will update password if password for user already exist and flash message indicating that it is update
    - otherise it will add a new password and flash message indicating that it is added

- Password submeuItems under Remove Nav Menu should remove password entry if it exist and flash message accordingly
- Password submeuItems under List Nav Menu should list all password entries from password table. truncate encrupted password to only 8 character while displaying it. If a partial email is given, refresh page to show only matching entry
- Password submeuItems under Update Nav Menu should update a selected user password
- Add a new Nav Menu "Check" and add a submenuItem Password to select a user with partial email and once selected, ask for the selected user password and flash message if it is valid or not.
    
    
# Add allowed files in Password table
- when first time user added, set the column 0 and set pasword file to random password
- all another colums, int failed_attempt. Increment it on every failed login. After 4 failed login, set allowed filed to 0
- any point of time, when password ic changed, set it to one


---------------
# Add a Referrer model class

## 1. Add a new model Referrer in models.py with following attributes

  user_id : Foreigky yo  User.id, unique
  full_name : 64 character string, required, indexed
  mobile: integer, optional, indexed, primary key
  email: optional email type, indexed, optional
  batch: 16 character string, optional
  referrer_id: integer, optional,

## 2. Add referrer attribute in User model class with relationship with Referrer.user_id and add user attribute in Referrer class to have relationship with User.referrer

## 3. under Update Navigation Menu, add Referrer submenuItem to search a Refreree using User.username, Contact.email or Contact.mobile. Once user is listed, show update button to update all attributes of Referrer model class.
