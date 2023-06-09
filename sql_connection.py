import requests
import json
import os
from getmac import get_mac_address

API_HEADERS = { "MAC" : get_mac_address() }

device_id = 1
def check_if_authorized(card):# function returns true if authorized user otherwise false
    try:
        Users = { "Users": [ card ] }
        print(json.dumps(Users))
        AUTH_URL = "http://" + os.getenv('HOST', 'localhost') + ":8082/auth_user.php"
        auth_response = requests.post(AUTH_URL, headers=API_HEADERS, data=json.dumps(Users));
        if auth_response.status_code == 200:
            print(auth_response.text)
            print(auth_response.json())
            for user in auth_response.json():
                if ( auth_response.json()[user] == False ):
                    return False
            return True
        else:
            return False
    except Exception as e:
        print(repr(e))
        return False

def check_if_admin(card): #function returns true if admin
    try:
        Users = { "Users": [ card ] }
        print(json.dumps(Users))
        AUTH_URL = "http://" + os.getenv('HOST', 'localhost') + ":8082/auth_admin.php"
        auth_response = requests.post(AUTH_URL, headers=API_HEADERS, data=json.dumps(Users));
        if auth_response.status_code == 200:
            print(auth_response.text)
            print(auth_response.json())
            for user in auth_response.json():
                if ( auth_response.json()[user] == False ):
                    return False
            return True
        else:
            return False
    except Exception as e:
        print(repr(e))
        return False
    
def configurePi():#pull config data from SQL database
    try:
        CONFIG_URL = "http://" + os.getenv('HOST', 'localhost') + ":8082/config.php"
        config_response = requests.get(CONFIG_URL, headers=API_HEADERS)
        if config_response.status_code == 200:
            config_values = config_response.json()
            countDownMinutes = float(config_values['countDownMinutes']) # should be editable to change the length of the countdown
            endOfWorkingHours = float(config_values['endOfWorkingHours'])  # changes the end time of the makerspace working hours
            beginningOfWorkHours = float(config_values['beginningOfWorkHours'])  # changes the start time of the makerspace working hours
            twoSwipeTime = float(config_values['twoSwipeTime'])  #deault is 20sec change to give buddy more or less time to swipe after first swipe
            countDownIncrementer = countDownMinutes*60 #turns the number of minutes wanted into seconds
            TIMESTOBUZ = [float(time) for time in config_values['timesToBuzz']] # Array to buzz times minutes (can be non-integer)
            TIMETOTURNBUZZERON = float(config_values['buzzTime']) # Buzz length (seconds)
            return countDownIncrementer, endOfWorkingHours, beginningOfWorkHours, twoSwipeTime, TIMESTOBUZ, TIMETOTURNBUZZERON
    except Exception as e:
        print(repr(e))

def noBuddyAPICall(): # sends a event to the database to say they had no buddy swipe
    try:
        LOG_URL = "http://" + os.getenv('HOST', 'localhost') + ":8082/log.php"
        requests.post(LOG_URL, headers=API_HEADERS, data=json.dumps( { "Events" : ["Authentication Failed - No Buddy Swipe"] } ))
    except Exception as e:
        print(repr(e))
    
def SessionEndedAPICall(): # sends a event to the database to say they have ended their session
    try:
        LOG_URL = "http://" + os.getenv('HOST', 'localhost') + ":8082/log.php"
        requests.post(LOG_URL, headers=API_HEADERS, data=json.dumps( { "Events" : ["Session Ended"] } ))
    except Exception as e:
        print(repr(e))

def get_name(id):#pull config data from SQL database
    try:
        NAME_URL = "http://" + os.getenv('HOST', 'localhost') + ":8082/name.php"
        name_response = requests.get(NAME_URL, headers=API_HEADERS, data=json.dumps( { "Users" : [id] } ))
        if name_response.status_code == 200:
            return name_response.json()[id]
    except Exception as e:
        print(repr(e))
        return repr(e)
    return "UNKNOWN"
