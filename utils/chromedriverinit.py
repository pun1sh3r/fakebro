
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
import os
from instafake.utils.user_account import login


class BrowserDriverInit():
    def __init__(self):
        self.chrome_options = Options()
        self.prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096,
                 'intl.accept_languages': 'en-US'}
        self.chrome_options.add_argument('--dns-prefetch-disable')
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--lang=en-US')
        # chrome_options.add_argument('--headless')
        self.chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.capabilities = DesiredCapabilities.CHROME
        self.chrome_options = self.chrome_options
        self.capabilities = self.capabilities
        self.driver_location = os.environ['DRIVER_PATH']
        self.cookie_path = os.environ['COOKIE_PATH']

    def __enter__(self):
        try:
            self.browser = webdriver.Chrome(self.driver_location,
                                       desired_capabilities=self.capabilities,
                                       chrome_options=self.chrome_options)


        except Exception as exc:
            print('ensure chromedriver is installed at location'.format(
            ))
            raise exc
        login(self.browser)
        return self.browser



    def __exit__(self,exc_type,exc_value,traceback):
        self.browser.delete_all_cookies()
        self.browser.quit()

