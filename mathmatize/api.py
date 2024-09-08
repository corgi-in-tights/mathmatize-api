import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException

from typing import List

from .components import TaskRow, Task, Poll, Quiz
from .utils import get_web_element


class MathMatizeAPI:
    def __init__(self, chromedriver_path, email, password) -> None:
        self._setup_web_driver(chromedriver_path)
        self._sign_in(email, password)

    def _setup_web_driver(self, chromedriver_path):
        self.service = Service(chromedriver_path)
        self.service.start()
        self.driver = webdriver.Chrome(service=self.service)

    def _sign_in(self, email, password):
        self.driver.get('https://www.mathmatize.com/account/')

        get_web_element(
            self.driver, 
            EC.visibility_of_element_located, 
            "//input[@id='input-email']"
        ).send_keys(email)

        get_web_element(
            self.driver, 
            EC.visibility_of_element_located, 
            "//input[@id='input-password']"
        ).send_keys(password)

        time.sleep(0.5) # wait for inputs to fully register

        get_web_element(
            self.driver,
            EC.element_to_be_clickable,
            "//button[text()='SIGN IN' and contains(@class, 'mui-style-1fky9ur')]"
        ).click()

        get_web_element(
            self.driver,
            EC.visibility_of_element_located,
            "//button[text()='Sign Out']"
        ).click()


    def _identify_activity(self, activity_list, uuid, url):
        # identify what type of activity it is based on the avaliable elements
        try:
            activity_list.find_element(By.XPATH, ".//div[contains(@class, 'MuiGrid-root') and contains(@class, 'MuiGrid-item') and contains(@class, 'mui-style-1wxaqej')]")
            return Quiz(uuid, url)
            
        except NoSuchElementException:
            try:
                poll_rooms = activity_list.find_elements(By.XPATH, ".//a[contains(@class, 'MuiListItemButton-gutters')]")
            except NoSuchElementException:
                poll_rooms = []

            return Poll(uuid, url, poll_rooms)
            

    def _scrape_task_element(self, task_element):
        uuid = '-'.join(task_element.get_attribute('data-testid').split('-')[-5:])
        title = task_element.find_element(By.XPATH, ".//span").text
        url = task_element.get_attribute('href')

        # open activity list
        task_element.click()
        time.sleep(1.5) # opening animation >.>
        
        activity_list = get_web_element(
            self.driver,
            EC.visibility_of_element_located,
            "//div[contains(@class, 'MuiDialog-container')]"
        )

        activity = self._identify_activity(activity_list, uuid, url)        

        # close activity list
        activity_list.find_element(
            By.XPATH, 
            "//button[contains(@class, 'MuiButtonBase-root') and @aria-label='Close Assessment']"
        ).click()
        time.sleep(1) # closing animation <.<
 
        return Task(uuid, task_element, title, activity)


    def _scrape_row_element(self, row_element):
        # row metadata
        _id = re.search(r'(\d{4})', row_element.get_attribute('id')).group(1)
        title = row_element.find_element(By.XPATH, ".//span").text
        
        # tasks
        tasks = []
        try:
            root_element = row_element.find_element(By.XPATH, "..")
            task_elements = root_element.find_elements(
                By.XPATH, 
                ".//button[contains(@class, 'MuiButtonBase-root') and @data-testid]"
            )

            for el in task_elements:
                tasks.append(self._scrape_task_element(el))

        except NoSuchElementException:
            pass

        return TaskRow(_id, row_element, title, tasks)


    def scrape_classroom(self, classroom_id) -> List[TaskRow]:
        self.driver.get(f"https://www.mathmatize.com/c/{classroom_id}")

        time.sleep(2) # website loading

        try:
            row_elements = get_web_element(
                self.driver,
                EC.presence_of_all_elements_located,
                "//div[contains(@class, 'MuiAccordionSummary-gutters')]"
            )

            rows = []
            for el in row_elements:
                if (not el.get_attribute('aria-expanded')):
                    el.click()
                    time.sleep(0.3) # animation
                rows.append(self._scrape_row_element(el))
            
            return rows
        
        except NoSuchElementException:
            return []

