\# parse registration text and fill up user registration form to submit registration table.



\## Below registration text will be provided in form rendered by /reg\_from\_wa\_text route. When 'Register' button is clicked, the data will be fed to functions.parse\_wa\_text.py to format in desired type and a dict USERDICT will be created.



\*STUDENT DETAILS FOR GLB-B03 BATCH\*

======================================

Full Name: Mohamad Salah

Mobile: +91-123 45 6789

WhatsApp: +91-12345-6789

Gender: Male

——————————————

HOMETOWN DETAILS

Country:India

State: Telangana

District: Hydrabad

Town/City: Toli	

——————————————

CURRENT RESIDENCE

Country: Egypt

State: Cairo

City: Badr

Area:BadrStreet

——————————————

OTHER DETAILS

Year of birth: 1979

Education: Mbbs

Profession: Medical Doctor 

Email Address: doctor@doctor.eg

——————————————

REFERRED By

Full Name: Ronaldo

Mobile#: +39-8768768-4

Email#:messi@mess.com

Student ID#: 304

Batch#: qtr

——————————————



\## 3. Once USERDICT is created, /reg\_from\_wa\_text route will be called to render the UserRegForm with auto filled value.  A person  will correct the values and submit the  /reg\_from\_wa\_text form for user registration.

