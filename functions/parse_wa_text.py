#
import re

# text = """
# some junk text here
# *STUDENT DETAILS FOR GLB-B02 BATCH*
# ======================
# Full Name :  Joe Samual
# Mobile# : +1-076687-876
# WhatsApp# : +91-123-456876
# Gender : Male
# ——————————————
# HOMETOWN DETAILS
# Town/City : Raheem NAGER
# District : Lucknow
# State : U.P
# Country : India
# ——————————————
# CURRENT RESIDENCE
# City : Bollywood
# State : New York
# Country : Usa
# Pin/Zip : ZXZ-123
# ——————————————
# OTHER DETAILS
# Year of birth : 1973
# Qualification : Be
# Profession : Profession in University
# Email Address : myemail@gmail.com
# ——————————————
# REFERRED By : 
# Full Name : Raju Smith
# Mobile# : +61-876-8763
# Student ID# : 784
# Batch# : HYD-07
# ——————————————
# some junk text here
# """

# Initialize the dictionary
USERDICT = {
    'batch': None,
    'email': None,
    'name': None,
    'gender': None,
    'yob': None,
    'mobile': None,
    'whatsapp': None,
    'hometowncity': None,
    'hometowndistrict': None,
    'hometownstate': None,
    'hometowncountry': None,
    'residencecity': None,
    'residencestate': None,
    'residentcountry': None,
    'residentzip': None,
    'education': None,
    'profession': None,
    'referrer_id': None,
}

# Function to capitalize person and place names
def capitalize_name(name):
    return ' '.join([word.capitalize() for word in name.split()])

# Function to remove non-numeric characters from phone numbers
def clean_phone(number):
    return re.sub(r'\D', '', number)

# Parse the text and update USERDICT
def parse_wa_text_fn(text):
    """Extract student details"""
    user_details = re.search(r'\STUDENT DETAILS FOR[\s\S]+?REFERRED By :', text)

    if user_details:
        user_details1 = re.search(r'STUDENT DETAILS FOR[\s\S]+?CURRENT RESIDENCE', text)
        details = user_details1.group()

        # Extract batch (GLB-B03)
        batch_match = re.search(r'\*STUDENT DETAILS FOR (.*) BATCH\*', text)
        if batch_match:
            USERDICT['batch'] = batch_match.group(1).strip()

        # Extract name
        name_match = re.search(r'Full Name\s*:\s*(.*)', details)
        if name_match:
            USERDICT['username'] = capitalize_name(name_match.group(1).strip())

        # Extract mobile
        mobile_match = re.search(r'Mobile#\s*:\s*(.*)', details)
        if mobile_match:
            USERDICT['mobile'] = clean_phone(mobile_match.group(1))

        # Extract WhatsApp
        whatsapp_match = re.search(r'WhatsApp#\s*:\s*(.*)', details)
        if whatsapp_match:
            USERDICT['whatsapp'] = clean_phone(whatsapp_match.group(1))

        # Extract gender
        gender_match = re.search(r'Gender\s*:\s*(\w+)', details)
        if gender_match:
            gender = gender_match.group(1).strip().lower()
            USERDICT['gender'] = 'M' if gender == 'male' else 'F'

        # Extract hometown details
        hometown_city = re.search(r'Town/City\s*:\s*(.*)', details)
        if hometown_city:
            USERDICT['hometowncity'] = capitalize_name(hometown_city.group(1).strip())

        hometown_district = re.search(r'District\s*:\s*(.*)', details)
        if hometown_district:
            USERDICT['hometowndistrict'] = capitalize_name(hometown_district.group(1).strip())

        hometown_state = re.search(r'State\s*:\s*(.*)', details)
        if hometown_state:
            USERDICT['hometownstate'] = hometown_state.group(1).strip().upper()

        hometown_country = re.search(r'Country\s*:\s*(.*)', details)
        if hometown_country:
            hometown_country = hometown_country.group(1).strip()
            if len(hometown_country) > 3:
                USERDICT['hometowncountry'] = capitalize_name(hometown_country)
            else:
                USERDICT['hometowncountry'] = hometown_country.upper()


        # user_details2 = re.search(r'CURRENT RESIDENCE[\s\S]+?REFERRED By :', text)
        user_details2 = re.search(r'CURRENT RESIDENCE[\s\S]+?.*$', text)
        details = user_details2.group()
        # Extract current residence details
        residence_city = re.search(r'City\s*:\s*(.*)', details)
        if residence_city:
            USERDICT['residencecity'] = capitalize_name(residence_city.group(1).strip())

        residence_state = re.search(r'State\s*:\s*(.*)', details)
        if residence_state:
            residence_state = residence_state.group(1).strip()
            if len(residence_state) > 3:
                USERDICT['residencestate'] = capitalize_name(residence_state)
            else:
                USERDICT['residencestate'] = residence_state.upper()

        residence_country = re.search(r'Country\s*:\s*(.*)', details)
        if residence_country:
            residence_country = residence_country.group(1).strip()
            if len(residence_country) > 3:
                USERDICT['residentcountry'] = capitalize_name(residence_country)
            else:
                USERDICT['residentcountry'] = residence_country.upper()

        # residence_zip = re.search(r'Pin/Zip\s*:\s*(\d+)', details)
        residence_zip = re.search(r'Pin/Zip\s*:\s*(.*)', details)
        if residence_zip:
            USERDICT['residentzip'] = residence_zip.group(1).strip()

        # Extract year of birth
        yob_match = re.search(r'Year of birth\s*:\s*(\d+)', details)
        if yob_match:
            USERDICT['yob'] = yob_match.group(1).strip()

        # Extract education
        education_match = re.search(r'Qualification\s*:\s*(.*)', details)
        if education_match:
            education = education_match.group(1).strip()
            if len(education) > 3:
                USERDICT['education'] = capitalize_name(education)
            else:
                USERDICT['education'] = education.upper()

        # Extract profession
        profession_match = re.search(r'Profession\s*:\s*(.*)', details)
        if profession_match:
            USERDICT['profession'] = profession_match.group(1).strip()

        # Extract email
        email_match = re.search(r'Email Address\s*:\s*(.*)', details)
        if email_match:
            USERDICT['email'] = email_match.group(1).strip().lower()

        # Extract referrer details
        referrer_id_match = re.search(r'Student ID#\s*:\s*(.*)', details)
        if referrer_id_match:
            USERDICT['referrer_id'] = referrer_id_match.group(1).strip()
    return USERDICT

# # Run the parser
# parse_wa_text(text)
