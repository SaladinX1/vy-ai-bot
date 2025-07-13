import pickle
from vision.actions import click_text, type_text, wait_for_element
from utils.email_reader import read_latest_code
from utils.logger import append_log

def save_cookies(driver, path):
    pickle.dump(driver.get_cookies(), open(path, "wb"))

def load_cookies(driver, path):
    for c in pickle.load(open(path, "rb")):
        driver.add_cookie(c)

def login_with_2fa(email, password):
    wait_for_element("Email")
    type_text(email)
    click_text("Next")
    wait_for_element("Password")
    type_text(password)
    click_text("Sign in")

    code = read_latest_code(email)
    if code:
        type_text(code)
        click_text("Verify")
        append_log("[LOGIN] 2FA réussi")
    else:
        append_log("[LOGIN] Échec de récupération code 2FA")
