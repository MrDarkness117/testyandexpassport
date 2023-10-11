from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import inspect


class BaseElement(object):
    def __init__(self, driver, locator, logs=None):
        self.driver = driver
        self.url = ''
        self.locator = locator
        self.logs = logs

        self.web_element = None
        self.find()

    def find(self) -> None:
        element = WebDriverWait(self.driver, 15)\
            .until(EC.visibility_of_element_located(locator=self.locator))
        self.web_element = element
        frame = inspect.currentframe()
        self.logs.log(f"Find element '{inspect.getouterframes(frame, 3)[3][3]}'.")

    def input_text(self, txt: str) -> None:
        self.web_element.send_keys(txt)
        self.logs.log(f"Input text '{txt}' into found element.")

    def clear_text(self) -> None:
        self.web_element.clear()
        self.logs.log(f"Clear text of the element")

    def attribute(self, attr_name: str) -> str:
        attribute = self.web_element.get_attribute(attr_name)
        self.logs.log(f"Get attribute '{attr_name}' from found element.")
        return attribute

    def click(self) -> None:
        element = WebDriverWait(self.driver, 15)\
            .until(EC.element_to_be_clickable(self.locator))
        element.click()
        frame = inspect.currentframe()
        self.logs.log(f"Click found element.")

    def hover_center(self) -> None:
        frame = inspect.currentframe()
        self.logs.log(f"Hover mouse over element {inspect.getouterframes(frame, 5)[3][3]}")
        element = WebDriverWait(self.driver, 15)\
            .until(EC.visibility_of_element_located(locator=self.locator))
        actions = ActionChains(driver=self.driver)
        actions.move_to_element(element).perform()  # set the cursor to be in the middle

    def hover_offset(self, x: int = 0, y: int = 0) -> None:
        frame = inspect.currentframe()
        self.logs.log(f"Hover mouse over element {inspect.getouterframes(frame, 5)[3][3]} with offset: x: '{x}', y: '{y}'")
        actions = ActionChains(driver=self.driver)
        actions.move_by_offset(x, y).perform()

    def hover_center_and_click(self) -> None:
        frame = inspect.currentframe()
        self.logs.log(f"Hover mouse over element {inspect.getouterframes(frame, 5)[3][3]} center and click.")
        element = WebDriverWait(self.driver, 15) \
            .until(EC.visibility_of_element_located(locator=self.locator))
        actions = ActionChains(driver=self.driver)
        actions.move_to_element(element).click().perform()  # set the cursor to be in the middle

    def hover_center_offset_and_click(self, x=0, y=0) -> None:
        frame = inspect.currentframe()
        self.logs.log(f"Hover mouse over element {inspect.getouterframes(frame, 5)[3][3]} with offset and click.")
        element = WebDriverWait(self.driver, 15)\
            .until(EC.visibility_of_element_located(locator=self.locator))
        actions = ActionChains(driver=self.driver)
        actions.move_to_element(element).move_by_offset(x, y).click().perform()

    @property
    def text(self):
        text = self.web_element.text
        return text
