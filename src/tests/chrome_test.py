import unittest
import re
from src.tests.config import config_data
"""Install selenium in project interpreter"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *


class ChromeTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(r"drivers/linux/chromedriver")
        self.driver.maximize_window()
        self.driver.get(config_data['website_location'])

    def testOptions(self):
        """
        Test the language options.
        :raise: NoSuchElementException if the language option is not present.
        """
        self.assertEqual(self.driver.current_url, config_data['website_location'])
        link2 = self.driver.find_element_by_id('options')
        link2.click()
        try:
            self.driver.find_element_by_partial_link_text('Nederlands')
        except NoSuchElementException:
            try:
                self.driver.find_element_by_partial_link_text('English')
            except NoSuchElementException:
                self.fail('Failed to find language option')

    def testProjects(self):
        """
        Test the projects page.
        :raise: TimeoutException if the projects page does not load.
        :raise: NoSuchElementException if there are no projects on the projects page.
        """
        link1 = self.driver.find_element_by_partial_link_text('Projects')
        link1.click()
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(lambda browser: self.driver.current_url == config_data['website_location'] + 'projects')
        except TimeoutException:
            self.fail("Loading timeout for project link expired")
        """Test whether there are elements present"""
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(lambda browser: self.driver.find_element_by_class_name("card-body"))
        except NoSuchElementException:
            self.fail('No projects present on projects page')
        #TODO test all other options: filter, descr, project click

    def testSearch(self):
        """

        :raise: TimeoutException if search fails.
        :raise: NoSuchElementException if searched projects is not found.
        """
        self.driver.get(config_data['website_location'] + 'projects')
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda browser: self.driver.find_element_by_class_name("card-body"))
        search_bar = self.driver.find_element_by_id('search_text')
        search_bar.send_keys('audio')
        self.driver.find_element_by_id("search_submit").click()
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(lambda browser: self.driver.current_url == config_data['website_location'] +
                           'projects?page=0&amount=50&edit=false&search=audio')
        except TimeoutException:
            self.fail("Loading timeout for search link expired")
        try:
            self.driver.find_element_by_partial_link_text('AUDIO: MODEL BASED AUDIO PROCESSING (MBAP)') # TODO mag eigenlijk niet, wat als project er niet is
        except NoSuchElementException:
            self.fail("Audio project not found, search not working")

    def testLogin(self):
        """
        Tests whether the login function works.
        :raise: TimeoutException if the login fails.
        """
        login_link = self.driver.find_element_by_id('login')
        login_link.click()
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(lambda browser: self.driver.current_url == config_data['website_location'] + 'login' or
                       self.driver.current_url == config_data['website_location'] + 'login?')
        except TimeoutException:
            self.fail("Loading timeout for login link expired")
        self.driver.find_element_by_id('username').send_keys(config_data['student_user'])
        self.driver.find_element_by_id('password').send_keys(config_data['student_password'])
        self.driver.find_element_by_id('submit').click()
        self.assertEqual(self.driver.current_url, config_data['website_location'])

    def testScenario1(self):
        """
        Employee creates project.
        Student enlists for a project and guide accepts and rejects.
        :raise:
        """
        """Creating project as employee"""
        """Login"""
        self.driver.get(config_data['website_location'] + "login")
        self.driver.find_element_by_id('username').send_keys(config_data['employee_user'])
        self.driver.find_element_by_id('password').send_keys(config_data['employee_password'])
        self.driver.find_element_by_id('submit').click()
        self.assertEqual(self.driver.current_url, config_data['website_location'])
        self.driver.find_element_by_partial_link_text("Projects").click()
        self.assertEqual(self.driver.current_url, config_data['website_location'] + "projects")
        """Creating"""
        self.driver.find_element_by_id("submitbutton").click()
        self.assertEqual(self.driver.current_url, config_data['website_location'] + "project-page?new=true")
        self.driver.find_element_by_id("title").send_keys("Test ")
        dropdowns = self.driver.find_elements_by_class_name("bootstrap-select")
        for dropdown in dropdowns:
            dropdown.click()
            try:
                self.driver.find_element_by_partial_link_text("No research group").click()
            except NoSuchElementException:
                try:
                    self.driver.find_element_by_partial_link_text("Bachelor dissertation").click()
                except NoSuchElementException:
                    self.fail("Could not select project type during project creation")
        self.driver.find_element_by_id("generate-tags-btn").click()
        self.driver.find_element_by_id("description").send_keys("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.driver.find_element_by_xpath("//input[@placeholder='Add an employee']").send_keys(config_data['employee_name'])
        try:
            self.driver.find_elements_by_tag_name("li")[0].click()
        except NoSuchElementException:
            self.fail("Failed to select a guide for the project.")
        buttons = self.driver.find_elements_by_tag_name('button')
        for button in buttons:
            print(button.get_attribute("innerHTML"))
        try:
            self.driver.find_element_by_xpath('//button[text()="Yes"]').click()
        except NoSuchElementException:
            pass
        self.assertEqual(self.driver.current_url[-12], "success=true")
        """Logout"""
        self.driver.find_element_by_id("logout").click()
        self.assertEqual(self.driver.current_url, config_data['website_location'])
        """Student: Login"""
        self.driver.get(config_data['website_location'] + "login")
        self.driver.find_element_by_id('username').send_keys(config_data['student_user'])
        self.driver.find_element_by_id('password').send_keys(config_data['student_password'])
        self.driver.find_element_by_id('submit').click()
        self.assertEqual(self.driver.current_url, config_data['website_location'])
        """Student: Search for project"""
        self.driver.find_element_by_partial_link_text("Projects").click()
        self.assertEqual(self.driver.current_url, config_data['website_location'] + "projects")
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda browser: self.driver.find_element_by_class_name("card-body"))
        search_bar = self.driver.find_element_by_id('search_text')
        search_bar.send_keys('Test Project Title')
        self.driver.find_element_by_id("search_submit").click()
        try:
            project = self.driver.find_element_by_id("card-title0")
        except NoSuchElementException:
            self.fail("Could not find newly made project")
        project_id = re.findall('\d+', project.get_attribute("href"))[-1]
        """Student: Register"""
        project.click()
        self.assertEqual(self.driver.current_url, config_data['website_location'] + "project-page?project_id=" +
                         project_id)
        self.driver.find_element_by_id("registration-btn").click()

    def tearDown(self):
        self.driver.close()