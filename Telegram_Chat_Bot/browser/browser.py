# browser.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class Browser:
    def __init__(self, browser_choice):
        self.browser_choice = browser_choice
        self.driver = None

    def setup_driver(self):
        if self.browser_choice == 'chrome':
            options = ChromeOptions()
            options.add_argument("--headless")
            service = ChromeService('path/to/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=options)
        elif self.browser_choice == 'firefox':
            options = FirefoxOptions()
            options.add_argument("--headless")
            service = FirefoxService('path/to/geckodriver')
            self.driver = webdriver.Firefox(service=service, options=options)
        elif self.browser_choice == 'edge':
            options = EdgeOptions()
            options.add_argument("--headless")
            service = EdgeService(r'browsers/edgedriver_win64/msedgedriver.exe')
            self.driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError("Поддерживаемые браузеры: chrome, firefox, edge.")

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
