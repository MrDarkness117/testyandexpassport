from .base.core_locators import CoreLocators


class YandexPage(CoreLocators):

    url = "https://passport.yandex.ru"

    @property
    def mail_field(self):
        return self.CLASS_NAME("Textinput-Control")

    @property
    def phone_field(self):
        return self.CLASS_NAME("Textinput-Control")

    @property
    def login_button(self):
        return self.ID("passp:sign-in")

    @property
    def login_next_button(self):
        return self.ID("passp:phone:controls:next")

    @property
    def password_field(self):
        return self.NAME("passwd")

    @property
    def submit_password_button(self):
        return self.XPATH("//button[@data-t='button:action:passp:sign-in']")

    @property
    def mail_field_button(self):
        return self.XPATH("//span[text()='Почта']/..")

    @property
    def phone_field_button(self):
        return self.XPATH("//span[text()='Телефон']/..")

    @property
    def error_icon(self):
        return self.CLASS_NAME("Field-errorIcon")

    @property
    def sms_code_field(self):
        return self.ID("passp-field-phoneCode")

    @property
    def previous_step_button(self):
        return self.CLASS_NAME("PreviousStepButton")

    @property
    def create_new_id(self):
        return self.ID("passp:exp-register")

    @property
    def create_new_id_for_myself(self):
        return self.CLASS_NAME("RegistrationButtonPopup-itemButton")

    @property
    def button_text_span(self):
        return self.TEXT("*", "Продолжить")

    @property
    def phone_field_placeholder(self):
        return self.CLASS_NAME("Field-unvoiced-placeholder")
