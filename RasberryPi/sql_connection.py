BackUp_USER= {200248706, 200289830}
def check_if_authorized(card):# function returns true if authorized user otherwise false
    authorized = False #returns true if authorized user otherwise false
    #write user compatison code for sql in this
    if card in BackUp_USER:
        authorized = True
    return authorized