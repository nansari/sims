# Add classes in models.py

- add gender attribute in User class. Valid options are Config.GENDERS

- Add Email model that inherits BaseModel class having following coulmns:
 user_id : ForeignKey to User.id, it should be unique.
 email
 
- Replace email attribute in User class to refer Email class

- Add Mobile model that inherits BaseModel class having following coulmns:
 user_id : ForeignKey to User.id, it should be unique.
 mobile: 12 digit integer 
 
- Add WhatsApp model that inherits BaseModel class having following coulmns:
 user_id : ForeignKey to User.id, it should be unique.
 whatsapp: 12 digit integer 
 
- Add HomeAddress class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, it should be unique.
country_id: Should be one of Countries.id
state_id: should be one of States.id realted to Countries.id
citi_id: should be one of Cities.id realted to States.id
area: 32 character text
zip: 32 character text

- Add ResidentAddress class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, it should be unique.
country_id: Should be one of Countries.id
state_id: should be one of States.id realted to Countries.id
citi_id: should be one of Cities.id realted to States.id
area: 32 character text
zip: 32 character text


- Add OtherDeatils class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, it should be unique
education : 32 character text
profession : 32 character text
visa_status : 32 character text, optional
citizenship: 32 character text, optional, optional
spouse: single digit integer, , optional
son: single digit integer, optional
daughter: single digit integer, optional

- Add ProgressRecord class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, duplicate allowed
note: A pragraph of text

- Add AttendanceStatus class that inherits BaseModel class having following coulmns:
status : single character alpha

- Add ClassSesion that inherits BaseModel class having class_date & class_batch_id . Combination of these two should be unique and no duplicate combination allowed.

- Add UserAttendance class that inherits BaseModel class having following coulmns: Combination of user_id and class_session_id should be unique
user_id : ForeignKey to User.id
class_session_id : foreign key to ClassSesion.id
status: one of possible status from AttendanceStatus.status

- Add AttendanceFeedback class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, duplicate allowed
class_session_id : foreign key to ClassSesion.id
note: A pragraph of text

-Add RegistrationStatus class that inherits BaseModel class having following coulmns:
status: 16 Character

- Add UserRegistrationStatus class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, duplicate allowed
status : foreign key to RegistrationStatus.id
note: Add the notes to ProgressRecord.note column whenever status changes

- Add CallOutTime class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, duplicate allowed
hours: hh:mm format
timezone: 16 cahractyer text

- Add Photo class that inherits BaseModel class having following coulmns:
user_id : ForeignKey to User.id, Unique
pic: large binary data

- Add TestSession class that inherits BaseModel class having:
test_date & class_batch_id . Combination of these two should be unique and no duplicate combination allowed.
max_score: integer beetween 0 to 999

- Add TestSessionScore class that inherits BaseModel class 
test_session_id : TestSession.id
user_id :  ForeignKey to User.id
score: interger beetween o to TestSession.max_score
note: a line of text

- Add Task class that inherits BaseModel class. 
name: 64 character text
description: three paraa rich text
class_batch_id : ForeignKey to ClassBatch.id
due_date:

- Add TaskSubmissionStatus class that inherits BaseModel class. 
user_id :  ForeignKey to User.id
task_id : ForeignKey Task.id
done: 0 or 1
note: a line of text

- Skill

- Dual

-Aaamal