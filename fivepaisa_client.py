import pyotp
from py5paisa import FivePaisaClient
import config

def get_client(totp):
    totp = totp
    pin=config.PIN
    client_code=config.CLIENT_CODE
    cred = {
        "APP_NAME": config.APP_NAME,
        "APP_SOURCE": config.APP_SOURCE,
        "USER_ID": config.USER_ID,
        "PASSWORD": config.PASSWORD,
        "USER_KEY": config.USER_KEY,
        "ENCRYPTION_KEY": config.ENCRYPTION_KEY,

    }

    CLIENT = FivePaisaClient(cred=cred)
    login_response = CLIENT.get_totp_session(client_code,pin=pin)
    if login_response["status"]!="Success":
        raise Exception(f"login failed with {login_response}")

    print(f"login success with {login_response}")




    return CLIENT