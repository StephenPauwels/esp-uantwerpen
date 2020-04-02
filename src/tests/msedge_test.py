import unittest
"""Install selenium in project interpreter"""
from selenium import webdriver


class MSEdgeTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(r"drivers/msedgedriver.exe")
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")

    def tearDown(self):
        self.driver.close()