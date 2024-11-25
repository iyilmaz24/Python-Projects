def validate_form(name, age, phone_number, security_level, login_password):
    
    inputErrors = []
    
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