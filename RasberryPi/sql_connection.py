import requests
import json
from getmac import get_mac_address

API_HEADERS = { "MAC" : get_mac_address() }

device_id = 1
BackUp_USER= {200248706, 200289830}
def check_if_authorized(card):# function returns true if authorized user otherwise false
    try {
        Users = { "Users": [ card ] }
        print(json.dumps(Users))
        AUTH_URL = "http://localhost:8082/auth_user.php"
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
    } catch (Exception e) {
        print(repr(e))
        return False
    }
