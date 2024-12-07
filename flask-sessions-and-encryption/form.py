from db import get_db_con

def validate_newuser_form(username, name, age, phone_number, security_level, login_password, encrypted_username):
    inputErrors = []    
    
    if not username or username.isspace():
        inputErrors.append("You can not enter in an empty username.")
    else:
        db, cursor = get_db_con()
        cursor.execute('SELECT COUNT(*) AS count FROM users WHERE Username = ?', (encrypted_username,))
        resultUsername = cursor.fetchone()
        if resultUsername['count'] != 0:
            inputErrors.append("This username is not available.")
    
    if not name or name.isspace():
        inputErrors.append("You can not enter in an empty name.")
    
    if not phone_number or phone_number.isspace():
        inputErrors.append("You can not enter in an empty phone number.")
        
    if not age.isdigit() or not (0 < int(age) < 121):
        inputErrors.append("The age must be a whole number between 1 and 120.")
        
    if not security_level.isdigit() or not (1 <= int(security_level) <= 3):
        inputErrors.append("Security level must be a numeric value between 1 and 3.")
        
    if not login_password or login_password.isspace():
        inputErrors.append("You can not enter in an empty password.")
            
    return inputErrors


def validate_newentry_form(item_name, num_excellent_votes, num_ok_votes, num_bad_votes):
    inputErrors = []    
    
    if not item_name or item_name.isspace():
        inputErrors.append("You can not enter in an empty item name.")
    else:
        db, cursor = get_db_con()
        cursor.execute('SELECT COUNT(*) AS count FROM entries WHERE baking_item_name = ?', (item_name,))
        resultUsername = cursor.fetchone()
        if resultUsername['count'] != 0:
            inputErrors.append("This name is already being used by another entry.")
        
    if not num_excellent_votes.isdigit() or not (0 <= int(num_excellent_votes)):
        inputErrors.append("The # of excellent votes must be a whole number greater than 1.")
        
    if not num_ok_votes.isdigit() or not (0 <= int(num_ok_votes)):
        inputErrors.append("The # of OK votes must be a whole number greater than 1.")
        
    if not num_bad_votes.isdigit() or not (0 <= int(num_bad_votes)):
        inputErrors.append("The # of bad votes must be a whole number greater than 1.")
            
    return inputErrors