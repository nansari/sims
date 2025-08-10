# User Registration Implementation Instructions

Implement the user registration feature for the `/user_reg` route using the `user_reg.html` template.

---

## 1. Class and Batch Selection

- **Class Selection:**  
  The "Select Class" field must be a dropdown populated from the `ClassName` model.  
  *Requirement:* The dropdown height should be compact, with no excessive blank space after the last class name.

- **Batch Selection:**  
  When a class is selected, the "Select Batch" dropdown must display only the batches associated with the selected class.  
  *Requirement:* The dropdown height should be compact, with no excessive blank space.

---

## 2. Gender Selection

- The "Gender" dropdown must only show two options (M, F) and should not have unnecessary blank lines.

---

## 3. Field Instructions and Help

- In `UserRegForm` (`forms.py`), display an icon next to each of the following fields.  
  On hover or click, show the corresponding help/instruction text:

  | Field                              | Help Instruction                                                        |
  |-------------------------------------|-------------------------------------------------------------------------|
  | Mobile with country code            | No symbol or white space. Only integer e.g. 911234567890                |
  | WhatsApp with country code          | No symbol or white space. Only integer e.g. 911234567890                |
  | Referred By Mobile                  | No symbol or white space. Only integer e.g. 911234567890                |
  | Full Name                           | Full name of new user being registered                                  |
  | Gender                              | M or F                                                                  |
  | Mobile No of Referrer with country code | No symbol or white space. Only integer e.g. 911234567890            |

---

## 4. Hometown Address Fields

- **Hometown Country:** Dropdown from `Countries` model.
- **Hometown State:** Dropdown from `States` model, filtered by selected country.
- **Hometown District:** Dropdown from `Cities` model, filtered by selected state.
- **Hometown City:** Text field (not dropdown), max 32 characters.

---

## 5. Current Residence Address Fields

- **Current Residence Country:** Dropdown from `Countries` model.
- **Current Residence State:** Dropdown from `States` model, filtered by selected country.
- **Current Residence City:** Dropdown from `Cities` model, filtered by selected state.

---

## 6. Registration Status

- The "Registration Status" dropdown must show values from `UserStatusLookup.status`.
- The default value should be "Registration".
- The dropdown height should be compact, with no excessive blank space.

---

## 7. Validation

- In the `validate_username` method of `UserRegForm` (`forms.py`), ensure that the user being registered does not already exist.
- If the email or mobile number already exists in the database, treat the user as already existing.

---

## 8. Styling

- Use CSS and JavaScript to make `user_reg.html` modern, visually appealing, and user-friendly.