import zxcvbn

def check_password_strength(password, user_inputs=None):
    
    result  = zxcvbn.zxcvbn(password, user_inputs)
    return result["feedback"]["suggestions"]