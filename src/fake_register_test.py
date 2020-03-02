from lib.webdriver import Webdriver
from bs4 import BeautifulSoup

import yaml
import os
import re

import pytest
from fake_register import SavePage, RegisterGmail

class Test_SavePage:
    @pytest.fixture(scope='module')
    def obj_SavePage(self):
        yield SavePage()

    def test_load_config(self, obj_SavePage):
        yaml_file = obj_SavePage.load_config()
        assert isinstance(yaml_file, dict)

    @pytest.mark.timeout(60)
    def test_get_data(self, obj_SavePage):
        data = obj_SavePage.get_data()

        assert data is True
        assert os.path.exists('./page.html') is True

class Test_RegisterGmail:
    @pytest.fixture(scope='module')
    def obj_RegisterGmail(self):
        yield RegisterGmail()

    def test_load_config(self, obj_RegisterGmail):
        yaml_file = obj_RegisterGmail.load_config()
        assert isinstance(yaml_file, dict)
    
    def test_bs4(self, obj_RegisterGmail):
        with open('./page.html', 'r') as f:
            data = f.read()
        
        obj_RegisterGmail.bs4(data)
        self.soup = obj_RegisterGmail.soup
        
        assert isinstance(self.soup, BeautifulSoup)

    def test_get_name(self, obj_RegisterGmail):
        nome, sobrenome = obj_RegisterGmail._get_name()

        assert nome != '' and sobrenome != ''
        assert isinstance(nome, str) and isinstance(sobrenome, str)

    def test_get_email(self, obj_RegisterGmail):
        nome, sobrenome = obj_RegisterGmail._get_name()

        email = obj_RegisterGmail._get_email(nome, sobrenome)

        assert '{}{}@gmail.com'.format(nome, sobrenome).lower().replace(' ', '') == email

    def test_get_pass(self, obj_RegisterGmail):
        password = obj_RegisterGmail._get_pass()

        assert password is not None

    def test_register(self, obj_RegisterGmail):
        ret_error = obj_RegisterGmail.register()

        msg_error = ''
        assert ret_error.lower() == msg_error.lower()