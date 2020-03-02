from selenium import webdriver
import chromedriver_binary

class Webdriver:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

    def driver(self):
        return webdriver.Chrome(chrome_options=self.options)