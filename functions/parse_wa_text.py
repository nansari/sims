import re

# Initialize the dictionary
USERDICT = {
    'class_name': None,
    'batch_name': None,
    'full_name': None,
    'mobile': None,
    'whatsapp': None,
    'email': None,
    'gender': None,
    'hometown_country': None,
    'hometown_state': None,
    'hometown_district': None,
    'hometown_city': None,
    'resident_country': None,
    'resident_state': None,
    'resident_city': None,
    'yob': None,
    'education': None,
    'profession': None,
    'referrer_name': None,
    'referrer_mobile': None,
    'referrer_email': None,
    'referrer_batch': None,
    'referrer_student_id': None,
    'any_other_detail': "",
    'registration_status': 'NewRegistration',
}

def capitalize_name(name):
    """Capitalize each word in the name."""
    return ' '.join([word.capitalize() for word in name.split()])

def clean_phone(number):
    """Remove non-numeric characters from the phone number."""
    return re.sub(r'\D', '', number)

def parse_wa_text_fn(text):
    """Extract student details"""
    # Reset USERDICT
    for key in USERDICT:
        USERDICT[key] = None

    # Extract batch info
    batch_match = re.search(r'\*STUDENT DETAILS FOR (.*) BATCH\*', text)
    if batch_match:
        class_batch = batch_match.group(1).strip()
        class_batch = class_batch.split('-')
        if class_batch:
            USERDICT['class_name'] = class_batch[0].strip()
            USERDICT['batch_name'] = class_batch[1].strip() if len(class_batch) > 1 else ""
        else:
            USERDICT['class_name'], USERDICT['batch_name'] = ("", "")

    # Extract sections
    sections = re.split(r'—+', text)
    for section in sections:
        if 'HOMETOWN DETAILS' in section:
            parse_hometown(section)
        elif 'CURRENT RESIDENCE' in section:
            parse_residence(section)
        elif 'OTHER DETAILS' in section:
            parse_other_details(section)
        elif 'REFERRED By' in section:
            parse_referrer(section)
        else:
            parse_personal_details(section)

    return USERDICT

def parse_personal_details(section):
    name_match = re.search(r'Full Name:\s*(.*)', section)
    if name_match:
        USERDICT['full_name'] = capitalize_name(name_match.group(1).strip())

    mobile_match = re.search(r'Mobile:\s*(.*)', section)
    if mobile_match:
        USERDICT['mobile'] = clean_phone(mobile_match.group(1))

    whatsapp_match = re.search(r'WhatsApp:\s*(.*)', section)
    if whatsapp_match:
        USERDICT['whatsapp'] = clean_phone(whatsapp_match.group(1))

    gender_match = re.search(r'Gender:\s*(\w+)', section)
    if gender_match:
        gender = gender_match.group(1).strip().lower()
        USERDICT['gender'] = 'M' if gender.startswith('m') else 'F'

def parse_hometown(section):
    country_match = re.search(r'Country:\s*(.*)', section)
    if country_match:
        USERDICT['hometown_country'] = capitalize_name(country_match.group(1).strip())

    state_match = re.search(r'State:\s*(.*)', section)
    if state_match:
        USERDICT['hometown_state'] = capitalize_name(state_match.group(1).strip())

    district_match = re.search(r'District:\s*(.*)', section)
    if district_match:
        USERDICT['hometown_district'] = capitalize_name(district_match.group(1).strip())

    city_match = re.search(r'Town/City:\s*(.*)', section)
    if city_match:
        USERDICT['hometown_city'] = capitalize_name(city_match.group(1).strip())

def parse_residence(section):
    country_match = re.search(r'Country:\s*(.*)', section)
    if country_match:
        USERDICT['resident_country'] = capitalize_name(country_match.group(1).strip())

    state_match = re.search(r'State:\s*(.*)', section)
    if state_match:
        USERDICT['resident_state'] = capitalize_name(state_match.group(1).strip())

    city_match = re.search(r'City:\s*(.*)', section)
    if city_match:
        USERDICT['resident_city'] = capitalize_name(city_match.group(1).strip())

def parse_other_details(section):
    yob_match = re.search(r'Year of birth:\s*(\d+)', section)
    if yob_match:
        USERDICT['yob'] = yob_match.group(1).strip()

    education_match = re.search(r'Education:\s*(.*)', section)
    if education_match:
        USERDICT['education'] = capitalize_name(education_match.group(1).strip())

    profession_match = re.search(r'Profession:\s*(.*)', section)
    if profession_match:
        USERDICT['profession'] = capitalize_name(profession_match.group(1).strip())

    email_match = re.search(r'Email Address:\s*(.*)', section)
    if email_match:
        USERDICT['email'] = email_match.group(1).strip().lower()

def parse_referrer(section):
    name_match = re.search(r'Full Name:\s*(.*)', section)
    if name_match:
        USERDICT['referrer_name'] = capitalize_name(name_match.group(1).strip())

    mobile_match = re.search(r'Mobile#:\s*(.*)', section)
    if mobile_match:
        USERDICT['referrer_mobile'] = clean_phone(mobile_match.group(1))

    email_match = re.search(r'Email#:\s*(.*)', section)
    if email_match:
        USERDICT['referrer_email'] = email_match.group(1).strip().lower()

    student_id_match = re.search(r'Student ID#:\s*(\d+)', section)
    if student_id_match:
        USERDICT['referrer_student_id'] = student_id_match.group(1).strip()

    batch_match = re.search(r'Batch#:\s*(.*)', section)
    if batch_match:
        USERDICT['referrer_batch'] = batch_match.group(1).strip().upper()