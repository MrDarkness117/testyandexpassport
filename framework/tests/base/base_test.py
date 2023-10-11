import functools
import inspect
import json
import re

from logging import exception
from framework.functionality.verifier import Verifier

from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


from page_objects.base.logging_report import Logging, TakeScreenshot, LogReport
from page_objects.yandex_auth_page import YandexPage
from _default_paths.paths import paths


class BaseTest:

    def __init__(self, driver=webdriver.Chrome, manager=ChromeDriverManager):
        self.__driver_options = Options()
        self.logger = Logging()
        prefs = json.load(open(paths["config"] + "selenium_prefs.json", "r", encoding="utf-8"))
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.__driver_options.add_experimental_option('prefs', prefs)
        self.__driver_options.add_experimental_option('caps', caps)
        self.__manager = manager().install()
        self.driver = driver(service=Service(manager().install()))
        self.driver.maximize_window()
        self.driver.implicitly_wait(6)
        self.page = YandexPage(driver=self.driver, logs=self.logger)
        self.screenshot = TakeScreenshot(self, self.logger).take_screenshot
        self.verify = Verifier(logger=self.logger, screenshot=self.screenshot).verify

    def __process_browser_log_entry(self, entry):
        response = json.loads(entry['message'])['message']
        return response

    def _get_network_response_body(self):
        """
        Дополнительный метод для получения трафика из Selenium. Выдает огромный список всех взаимодействий в Network.
        Для него требуется сделать выгрузку по фильтру Fetch/XHR для правильной работы и донастроить execute_cpd_cmd.
        :return:
        """
        browser_log = self.driver.get_log('performance')
        events = [self.__process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if 'Network.responseReceived' in event['method']]
        # print(events)
        try:
            print(self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': events[0]["params"]["requestId"]}))
        except selenium_exceptions.WebDriverException as e:
            print(f"response.body is null: {e}")

    def test_case(func):
        """
        Пометка от автора:
            "Не придумал как сделать так чтобы объект Logger, Screenshot и driver оставались внутри одной инкапсуляции."
            "Поэтому создал такой декоратор, что как сирота из неблагополучной семьи попал в богатую и благополучную."
            "Да, он очень странный и странно себя ведёт... Но зато работает!" - Автор (я)

        Декоратор для отслеживания ошибок, создания скриншотов, остановки веб-драйвера.
        Этот декоратор блокирует возможность передачи параметров в методы типа "tst_". Поэтому параметризация невозможна
        TODO: Take this decorator out of class scope and make its elements accept Logger, Screenshot and driver objects.
        :return:
        """

        @functools.wraps(func)
        def wrapper(self):
            self.page.go()
            try:
                func(self)
            except Exception as e:
                self.screenshot()
                self.logger.log(f"FATAL: Test failed with error: {e}.")
                exception(e)
            self.logger.log("Finished. Closing webdriver.")
            self.driver.close()
            print("Exporting report.")
            curframe = inspect.currentframe()
            get_frame = fr"{inspect.getouterframes(curframe, 2)[2][1]}".split("\\")[-1].replace(".py", '')
            LogReport(testblock=get_frame, logs=self.logger.logs_text).test_results()
        return wrapper
