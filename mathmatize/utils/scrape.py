from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_web_element(driver, expectation, xpath, delay_seconds = 5):
    return WebDriverWait(driver, delay_seconds).until(expectation((By.XPATH, xpath)))