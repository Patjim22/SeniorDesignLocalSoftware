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
