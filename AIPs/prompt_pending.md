

# Add allowed files in Password table
- when first time user added, set the column 0 and set pasword file to random password
- all another colums, int failed_attempt. Increment it on every failed login. After 4 failed login, set allowed filed to 0
- any point of time, when password ic changed, set it to one