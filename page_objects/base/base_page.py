import inspect


class BasePage(object):
    """
    Pass in the URL for go()
    Передача URL в метод go()
    """

    url = None

    def __init__(self, driver, logs=None):
        self.driver = driver
        self.logs = logs

    def go(self):
        self.logs.log(f"Go to page: {self.url}")
        self.driver.get(self.url)

    def go_back(self):
        """
        На прошлую страницу, шаг назад
        :return:
        """
        self.logs.log(f"Go back to previous page in history.")
        self.driver.execute_script("window.history.go(-1)")

    def go_forward(self):
        """
        На прошлую страницу, шаг вперёд
        :return:
        """
        self.logs.log(f"Go forward to page in history.")
        self.driver.execute_script("window.history.go(1)")

    def go_to(self, num):
        """
        На страницу num (индекс страницы в истории браузера)
        :param num:
        :return:
        """
        self.logs.log(f"Go to page with index {num}")
        self.driver.execute_script("window.history.go({})").format(num)

    def refresh_page(self):
        """
        Обновить страницу методом JS window.history.go()
        :return:
        """
        self.logs.log(f"Refresh current page.")
        self.driver.execute_script("window.history.go(0)")