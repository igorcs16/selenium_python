#import sys
#sys.path.append('/')
from lib.webdriver import Webdriver
from bs4 import BeautifulSoup
from time import sleep

import yaml
import os

class SavePage:
    def __init__(self):
        self.driver = Webdriver().driver()
        self.config = self.load_config()

    def load_config(self):
        with open('resource/config.yml') as infile:
            return yaml.safe_load(infile)

    def get_data(self):
        try:
            os.remove('./page.html')
        except:
            pass
        
        try:            
            self.driver.get(self.config['url_fake_generator'])
            page = self.driver.page_source

            with open('./page.html', 'w+') as f:
                f.write(page)

            self.driver.quit()
            
            return True

        except Exception as e:
            raise e

class RegisterGmail:
    def __init__(self):
        self.driver = Webdriver().driver()
        self.config = self.load_config()

    def load_config(self):
        with open('resource/config.yml') as infile:
            return yaml.safe_load(infile)

    def bs4(self, data):
        self.soup = BeautifulSoup(data, 'html.parser')

    def _get_name(self):
        info_name = self.soup.select_one('.address h3').text.split(' ')
        return info_name[0], ' '.join(info_name[1:])

    def _get_email(self, nome, sobrenome):
        email = '{}{}@gmail.com'.format(nome, sobrenome)
        
        return email.lower().replace(' ', '')

    def _get_pass(self):
        extra = self.soup.select('.extra dl')
        passwd = [ i.dd.text for i in extra if 'Password' in i.dt ]

        return passwd

    def register(self):

        list_phones = [
            '+1 211122',
            '+55 00000',
            '+598 34511'
        ]

        with open('./page.html', 'r') as f:
            data = f.read()
        
        self.bs4(data)
        self.driver.get(self.config['url_gmail_register'])

        '''First page
            nome
            sobrenome
            email
            senha
        '''
        
        nome, sobrenome = self._get_name()
        email = self._get_email(nome, sobrenome)
        passwd = self._get_pass()
        
        #change window
        self.driver.find_element_by_xpath(self.config['xpaths']['button_create_account']).click()
        self.driver.switch_to_window(self.driver.window_handles[1])

        self.driver.find_element_by_xpath(self.config['xpaths']['input_name']).click()
        self.driver.find_element_by_xpath(self.config['xpaths']['input_name']).send_keys(nome)

        self.driver.find_element_by_xpath(self.config['xpaths']['input_lastName']).click()
        self.driver.find_element_by_xpath(self.config['xpaths']['input_lastName']).send_keys(sobrenome)

        self.driver.find_element_by_xpath(self.config['xpaths']['input_email']).click()
        self.driver.find_element_by_xpath(self.config['xpaths']['input_email']).send_keys(email)

        self.driver.find_element_by_xpath(self.config['xpaths']['input_pass']).click()
        self.driver.find_element_by_xpath(self.config['xpaths']['input_pass']).send_keys(passwd)

        self.driver.find_element_by_xpath(self.config['xpaths']['input_confirm']).click()
        self.driver.find_element_by_xpath(self.config['xpaths']['input_confirm']).send_keys(passwd)

        self.driver.find_element_by_xpath(self.config['xpaths']['input_next']).click()

        sleep(1)
        
        for i in list_phones:
            self.driver.find_element_by_xpath(self.config['xpaths']['input_number']).click()
            self.driver.find_element_by_xpath(self.config['xpaths']['input_number']).send_keys(i)

            self.driver.find_element_by_xpath(self.config['xpaths']['input_phoneNext']).click()
            
            validation = self.driver.find_element_by_xpath(self.config['xpaths']['field_msg_error'])
            
            ret = validation.text if validation.text else ''

            self.driver.find_element_by_xpath(self.config['xpaths']['input_number']).clear()

        self.driver.quit()
        
        return ret        
