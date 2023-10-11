import time

from framework.tests.base.base_test import BaseTest
from page_objects.yandex_auth_page import YandexPage

from framework.functionality.http_request import make_simple_http_request
from random import randrange


class LoginPageTests(BaseTest):

    def __init__(self):
        super().__init__()
        self.page = YandexPage(self.driver, logs=self.logger)  # Set up PageObject

    @BaseTest.test_case
    def tst_login_page_enter_symbols_mail(self):
        value_all_letters: str = "Abc123!#$%^&*()@ya.ru"
        value_max_letters: str = "test"*64 + "1"
        max_letters: int = 256
        self.page.mail_field.input_text(value_all_letters)
        actual_result: str = self.page.mail_field.attribute("value")
        self.verify(f"No letters are missing from the text field: '{value_all_letters}'. Actual: '{actual_result}'",
                    value_all_letters == actual_result)
        self.page.mail_field.input_text(value_max_letters)
        actual_result: str = self.page.mail_field.attribute("value")
        self.verify(f"Max letters is equal to '{max_letters}' - actual letter count: '{len(actual_result)}'",
                    max_letters == len(actual_result))

    @BaseTest.test_case
    def tst_login_page_verify_phone_field(self):
        data = make_simple_http_request("https://jsonplaceholder.typicode.com/users")
        phone_format_fetched = str(data[randrange(0, 6)]["phone"]).split(" ")[0]
        phone_format_with_letters = "абв79где1ты67163300"
        self.page.phone_field_button.click()
        self.page.phone_field.clear_text()
        self.page.phone_field.input_text(phone_format_fetched)
        expected_change = self.page.phone_field.attribute("value")
        self.verify(f"Phone number format has changed: '+' sign in new format: '{expected_change}'",
                    "+" in expected_change[0])
        self.verify(f"Phone number format has changed: '(' sign in new format: '{expected_change}'",
                    "(" in (expected_change[3] or expected_change[4] or expected_change[5]))
        self.page.phone_field.clear_text()
        self.page.phone_field.input_text(phone_format_with_letters)
        expected_change = "+7 (916) 716-33-00"
        actual_change = self.page.phone_field.attribute("value")
        self.verify(f"Phone number format has changed: '{expected_change}' vs '{actual_change}'",
                    expected_change in actual_change)

    @BaseTest.test_case
    def tst_login_page_does_not_authorize_without_password(self) -> None:
        expected_field_attribute: str = "field:input-passwd"
        expected_submit_button_attribute: str = "passp:sign-in"
        working_mail: str = "miromantsov@yandex.ru"
        data = make_simple_http_request("https://jsonplaceholder.typicode.com/users")
        new_data = data[randrange(0, 6)]["email"]  # Яндекс ругается на адреса почт из этой выборки, поэтому создаем костыль
        for addr in ["april.biz", "melissa.tv", "yesenia.net", "kory.org", "annie.ca", "jasper.info", "billy.biz"]:
            if addr in new_data:
                mail = new_data.replace(addr, "ya.ru")  # Костыль
        self.page.mail_field_button.click()
        self.page.mail_field.clear_text()
        self.page.mail_field.input_text(mail)
        self.page.login_button.click()
        try:
            self.verify(f"Page didn't find a random account, error icon detected.", self.page.error_icon is not None)
        except:
            pass
        self.page.refresh_page()
        self.page.mail_field_button.click()
        self.page.mail_field.input_text(working_mail)
        self.page.login_button.click()
        actual_field_attribute: str = self.page.password_field.attribute("data-t")
        actual_submit_button_attribute: str = self.page.password_field.attribute("data-t")
        self.verify(f"Page opened password field input.",
                    actual_field_attribute == expected_field_attribute)
        self.verify(f"Page changed the submit button attributes.",
                    actual_submit_button_attribute == expected_submit_button_attribute)
        self.page.password_field.input_text(data[1]["website"])
        self.page.submit_password_button.click()

    @BaseTest.test_case
    def tst_login_page_enter_abstract_code_from_sms(self):
        sms_value = "112233445566"
        expected_sms_value_2 = "123456"
        input_text_with_letters = "abc12def34gh56"
        data = make_simple_http_request("https://jsonplaceholder.typicode.com/users")[0]["phone"].split(' ')[0]
        self.page.phone_field_button.click()
        self.page.phone_field.clear_text()
        self.page.phone_field.input_text(data)
        self.page.login_button.click()
        self.page.sms_code_field.input_text(sms_value)
        expected_sms_code = self.page.sms_code_field.attribute("value")
        self.verify(f"SMS field contains only up to 6 numbers: {expected_sms_code}",
                    sms_value[:6] == expected_sms_code)
        self.page.previous_step_button.click()
        self.page.login_next_button.click()
        self.page.sms_code_field.input_text(input_text_with_letters)
        expected_sms_code = self.page.sms_code_field.attribute("value")
        self.verify(f"SMS field contains no letters: {expected_sms_code}",
                    expected_sms_code == expected_sms_value_2)

    @BaseTest.test_case
    def tst_login_page_create_new_id(self):
        expected_text = "Продолжить"
        expected_placeholder_text = "+7 (000) 000-00-00"
        expected_max_length = "6"
        self.page.create_new_id.click()
        self.page.create_new_id_for_myself.click()
        actual_text = self.page.button_text_span.text
        self.verify("Registration page has opened.",
                    actual_text == expected_text)
        data = make_simple_http_request("https://jsonplaceholder.typicode.com/users")[0]["phone"].split(' ')[0]
        self.page.phone_field.clear_text()
        actual_placeholder_text = self.page.phone_field_placeholder.text
        self.verify(f"Code field is available, placeholder visible: {actual_placeholder_text}",
                    expected_placeholder_text == actual_placeholder_text)
        self.page.phone_field.input_text(data)
        self.page.login_next_button.click()
        actual_max_length = self.page.sms_code_field.attribute('maxlength')
        self.verify(f"Max length of code field is: Actual: {actual_max_length}, Expected: {expected_max_length}",
                    expected_max_length == actual_max_length)

