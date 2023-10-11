from framework.tests.login_page_tests import LoginPageTests


def test():
    LoginPageTests().tst_login_page_does_not_authorize_without_password()


if __name__ == "__main__":
    test()
