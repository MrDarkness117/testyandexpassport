import datetime
import os

from _default_paths import paths as p
from _default_paths.paths import paths


def return_testblock(cls_name):
    """
    Статический метод возвращающий имя класса для сохранения файлов
    :param cls_name: Класс, имя которого мы должны получить
    :return:
    """
    return cls_name.__class__.__name__


class LogReport(object):
    """
    Составление отчетов о тестах. Действия сохраняются пошагово при помощи метода Logging().logger()
    testblock - Имя класса теста. Например, TestAuthPage
    logs - Вся сохраняемая информация о действиях драйвера
    """

    def __init__(self, testblock, logs, mode='s'):
        self.testblock = testblock
        self.logs = logs
        self.BASE_INFO = "SELENIUM ТЕСТИРОВАНИЕ - ДАТА/ВРЕМЯ: {} \n" \
                         "БЛОК ТЕСТИРОВАНИЯ - {}\n" \
                         "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ: \n" \
                         "{}".format(datetime.datetime.now(), self.testblock, self.logs)
        self.mode = mode
        if mode == 'g':
            self.BASE_INFO = ''

    def test_results(self):
        """
        Сохранение результатов тестирования в отдельный файл с информацией сохраненной в __init__()

        Использовать в блоке каждого тест кейса в самом конце:
            LogReport(testblock=RunClass(), logs=logging.log).test_results()

        где RunClass() - пример передаваемого название класса self.testblock для отчётов
        :return:
        """
        if not os.path.exists(paths['reports']):
            os.makedirs(paths['reports'])

        with open(paths['reports'] + self.testblock + ' ' +
                  str(datetime.datetime.now()).replace(':', '-')[:-7] + "_" +
                  '_report.txt', 'w', encoding='utf-8') as report:
            report.write(self.BASE_INFO)
        report.close()


class Logging(object):
    """
    Логгирование информации для блока LogReport().test_results()
    """
    logs_text = '=' * 90 + "\n"
    logs_text += "№  | Test step\n"
    logs_text += "_" * 100 + "\n"
    n = 0
    start_message = ''

    def start_msg(self, testblock):
        if __name__ == '__main__':
            self.start_message = "=" * 5 + "Начало тестирования."
        else:
            self.start_message = "=" * 5 + "Начало тестирования {}.".format(return_testblock(testblock))
        return self.start_message

    def log(self, report):
        """
        Сохранение информации в виде пошаговых логов
        Символы '/' и '=' говорят программе не сохранять эти логи как действия для воспроизведения,
        а носят исключительно информативный характер. Знак = для информации и предупреждений, / для ошибок

        Рекомендуется в начале файла run после импорта ставить следующие строки:
            logging = Logging()
            log = logging.logger
        где log - метод для логгирования шагов, информации и ошибок
        :param report: передаваемая информация
        :return:
        """
        if report[0] != '=':
            if report[0] != '/':
                self.n += 1
                self.logs_text += str(self.n) + '. | ' + report + "\n"
            else:
                self.logs_text += report + '\n'
        else:
            self.logs_text += report + '\n'


class TakeScreenshot(object):
    """
    Сохранение скриншотов
    """

    def __init__(self, testblock, logger=None):
        self.testblock = testblock
        self.driver = testblock.driver
        self.logger = logger

    def take_screenshot(self):
        """
        Использовать только с Selenium WebDriver
        Сохранить скриншот с именем self.testblock
        :return:
        """
        screenshots = paths["screenshots"]
        screenshot_name = screenshots + " " + return_testblock(self.testblock) + ' ' + \
                          str(datetime.datetime.now()).replace(':', '-')[:-7] + "_" + \
                          '_screenshot.png'
        print(screenshot_name)
        if not os.path.exists(screenshots):
            os.makedirs(screenshots)
        self.driver.save_screenshot(screenshot_name)
        self.logger.log(f"Screenshot '{screenshot_name}' exported to {screenshots}.")
