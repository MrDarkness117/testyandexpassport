from suites.suite_AuthPageTests import tst_login_page_does_not_authorize_without_password, tst_login_page_enter_symbols_mail, \
                                    tst_login_page_verify_phone_field, tst_login_page_create_new_id, tst_login_page_enter_abstract_code_from_sms


# Этот файл сделан в качестве примера, как можно запустить тесты.
# Тесты можно запустить и другими способами, соответственно.
tst_login_page_does_not_authorize_without_password.test()
tst_login_page_enter_symbols_mail.test()  # Пример теста с FAIL
tst_login_page_verify_phone_field.test()
tst_login_page_create_new_id.test()
tst_login_page_enter_abstract_code_from_sms.test()
