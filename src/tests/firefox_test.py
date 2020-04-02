import unittest
"""Install selenium in project interpreter"""
from selenium import webdriver


class FirefoxTests(unittest.TestCase):
    def test(self):
        self.driver = webdriver.Chrome(r"drivers/firefoxdriver.exe")
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")
        self.user = 's0123456'
        self.password = 'pass'
        self.driver.close()