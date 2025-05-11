import requests
import xml.etree.ElementTree as ET
from typing import Union
from Credentials import Credential


def logout(credential : Credential, timeout: int = 5) -> Union[bool, str]: 

    username = credential["username"]
    password = credential["password"]

    payload = {
        'mode': '193',
        'username': username,
        'password': password,
        'a': '1661062428616'
    }

    try:
        with requests.Session() as s:
            p = s.post('http://172.16.68.6:8090/httpclient.html', data=payload, timeout=timeout)
            if p.status_code == 200:
                xml_content = p.content
                root = ET.fromstring(xml_content)
                message_element = root.find('message')
                if message_element is not None:
                    message_text = message_element.text
                    if message_text == "You&#39;ve signed out":
                        return True
                else:
                    print("Message element not found.")
                    return False
            else:
                print("Error Response:", p)
                return False
            
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to logout {username}")
        return "Fail"
    
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return False