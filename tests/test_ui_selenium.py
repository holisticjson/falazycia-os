import os
os.environ['WDM_SSL_VERIFY'] = '0'

import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestStreamlitUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.base_url = 'http://localhost:8501'

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_home_title(self):
        self.driver.get(self.base_url)
        # Wait up to 15 seconds for the title to be loaded and set correctly
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.title_contains('Holistic AIDHD OS'))
        title = self.driver.title
        self.assertIn('Holistic AIDHD OS', title)

    def test_brain_dump_modal(self):
        self.driver.get(self.base_url)
        wait = WebDriverWait(self.driver, 15)
        
        # Wait until the Streamlit popover button is fully clickable
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'stPopover')]//button")))
        # Use Javascript click to bypass CSS fixed-position overlaps on Streamlit layouts
        self.driver.execute_script("arguments[0].click();", button)
        
        # Give half a second for popover animation
        time.sleep(0.5)
        
        # Verify that the popover modal is visible and displayed on the screen
        modal = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'stPopover')]")))
        self.assertTrue(modal.is_displayed())

if __name__ == '__main__':
    unittest.main()
