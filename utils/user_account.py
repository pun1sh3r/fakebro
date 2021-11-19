from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pickle
import os
from time import sleep

def check_cookie(browser,cookie_path):
    try:
        with open(f'{cookie_path}cookies-{os.environ["USERNAME"]}.pkl','rb') as cookie_jar:
            cookies = pickle.load(cookie_jar)
            for cookie in cookies:
                if isinstance(cookie.get('expiry'),float):
                    cookie['expiry'] = int(cookie['expiry'])
                browser.add_cookie(cookie)
            print("using existing cookie..")
            return True
    except Exception as ex :
        print(f"creating a new cookie logging in ... {ex}")
    return False



def login(browser):
    login_url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
    browser.get(login_url)
    hasCookie = check_cookie(browser, os.environ['COOKIE_PATH'])

    if not hasCookie:
        login_username = os.environ['USERNAME']
        login_password = os.environ['PASSWORD']
        login_url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
        browser.get(login_url)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "HmktE")))
        username = browser.find_element_by_xpath("//input[@name='username']")
        password = browser.find_element_by_xpath("//input[@name='password']")
        username.send_keys(login_username)
        password.send_keys(login_password)
        password.send_keys(Keys.RETURN)



    sleep(8)
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "XrOey")))
    except:
        print('login failed')
        return

    with open(f"{os.environ['COOKIE_PATH']}cookies-{username}.pkl", 'wb') as cookie_jar:
        cookies = browser.get_cookies()
        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
        pickle.dump(cookies, cookie_jar)
    print("logged in")



