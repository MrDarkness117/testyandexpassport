from .locator import Locator
from .base_page import BasePage
from .base_element import BaseElement
from selenium.webdriver.common.by import By


class CoreLocators(BasePage):

    def __init__(self, driver, url='https://passport.yandex.ru', logs=None):
        super().__init__(driver)
        self.url = url
        self.logs = logs

    def ID(self, value) -> BaseElement:
        """
        ID wrapper
        :return:
        """
        _locator = Locator(by=By.ID, value='{}'.format(value))
        return BaseElement(
            driver=self.driver,
            locator=_locator,
            logs=self.logs
        )

    def XPATH(self, value) -> BaseElement:
        """
        XPATH wrapper
        :return:
        """
        _locator = Locator(by=By.XPATH, value='{}'.format(value))
        return BaseElement(
            driver=self.driver,
            locator=_locator,
            logs=self.logs
        )

    def CLASS(self, value, tag='*') -> BaseElement:
        """
        Pseudo CLASS_NAME wrapper
        :param tag: нужен для указания тэгов, либо более полных указателей
        :param value: нужен для указания полного класса для поиска
        :return:
        """
        _locator = Locator(by=By.XPATH, value='//{}[@class="{}"]'.format(tag, value))
        return BaseElement(
            driver=self.driver,
            locator=_locator,
            logs=self.logs
        )

    def CLASS_NAME(self, value) -> BaseElement:
        """
        CLASS_NAME wrapper
        :param value: нужен для указания className
        :return:
        :param value:
        :return:
        """
        _locator = Locator(by=By.CLASS_NAME, value='{}'.format(value))
        return BaseElement(
            driver=self.driver,
            locator=_locator,
            logs=self.logs
        )

    def NAME(self, value) -> BaseElement:
        """
        NAME wrapper (Похоже NAME не работает)
        :return:
        """
        _locator = Locator(by=By.NAME, value='{}'.format(value))
        return BaseElement(
            driver=self.driver,
            locator=_locator,
            logs=self.logs
        )

    def TEXT(self,  value, tag="*", n='') -> BaseElement:
        """
        UNSAFE XPATH text() wrapper
        Может вызвать проблемы в поиске элемента, так как по умолчанию
        используется * для поиска конкретного элемента с id.
        :param n: нужен для указания id элемента
        :param tag: нужен для указания тэгов, либо более полных указателей
        :param value: нужен для указания текста для поиска
        :return:
        """
        _locator = Locator(by=By.XPATH, value='//{}[contains(text(), "{}")]{}'.format(tag, value, n))
        return BaseElement(
            driver=self.driver,
            locator=_locator,
            logs=self.logs
        )
