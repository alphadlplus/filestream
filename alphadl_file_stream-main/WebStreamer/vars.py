# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

from os import environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    MULTI_CLIENT = False
    API_ID = int(environ.get("API_ID"))
    API_HASH = str(environ.get("API_HASH"))
    API_KEY = str(environ.get("API_KEY"))
    API_URL = str(environ.get("API_URL"))
    BOT_TOKEN = str(environ.get("BOT_TOKEN"))
    
    MULTI_TOKEN1 = "6149689310:AAEhMVqL4_gueSY4SZQKkPQWaz5up1rP0Wg"
    MULTI_TOKEN2 = "6097033837:AAGWgl4l6a-C2eN78EFNr4ZvPSf_RbBovbc"
    MULTI_TOKEN3 = "6275103383:AAE9NqVEU079L1Kxwl6UcijJ0S5O_n94UNs"
    MULTI_TOKEN4 = "5867423825:AAFetk1sveOJCvvRsrnxjB4XG8vtLsfl-HQ"
    MULTI_TOKEN5 = "5991949045:AAG66MdvHEVLrSmylOQYuaFg9fpnQ5zY0s"

    OWNER_ID = [int(x) for x in environ.get("OWNER_ID", None).split(" ")]
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minte
    WORKERS = int(environ.get("WORKERS", "6"))  # 6 workers = 6 commands at once
    BIN_CHANNEL = int(
        environ.get("BIN_CHANNEL", None)
    )  # you NEED to use a CHANNEL when you're using MULTI_CLIENT
    PORT = int(environ.get("PORT", 8080))
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    HAS_SSL = environ.get("HAS_SSL", False)
    HAS_SSL = True if str(HAS_SSL).lower() == "true" else False
    NO_PORT = environ.get("NO_PORT", False)
    NO_PORT = True if str(NO_PORT).lower() == "true" else False
    USE_SESSION_FILE = str(environ.get("USE_SESSION_FILE", "0").lower()) in ("1", "true", "t", "yes", "y")
    if "DYNO" in environ:
        ON_HEROKU = True
        APP_NAME = str(environ.get("APP_NAME"))
    else:
        ON_HEROKU = False
    FQDN = "http://vip.alphadl.xyz/"
    # (
    #     str(environ.get("FQDN", BIND_ADDRESS))
    #     if not ON_HEROKU or environ.get("FQDN")
    #     else APP_NAME + ".herokuapp.com"
    # )
    if ON_HEROKU:
        URL = f"https://{FQDN}/"
    else:
        URL = "http{}://{}{}/".format(
            "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT)
        )
