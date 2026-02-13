import os

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement:
    def __init__(self, driver, selector):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.selector = selector

    def get_element(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.selector)
        )

    def get_attribute(self, atr_name):
        element = self.get_element()
        return element.get_attribute(atr_name)

    def click(self):
        element = self.get_element()
        element.click()

    def fill(self, text):
        element = self.get_element()
        try:
            element.clear()
        except:
            pass
        try:
            current_value = element.get_attribute("value") or ""
            for _ in range(len(current_value)):
                element.send_keys(Keys.BACKSPACE)
        except:
            pass
        assert element.get_attribute("value") == ""
        element.send_keys(text)
        return self

    def should_be_has_text(self, expected):
        element = self.get_element()
        actual = element.text.strip()
        assert actual == expected, f"ACTUAL IS:  {actual}, EXPECTED IS: {expected}"

    def should_contain_text(self, expected):
        actual_text = self.get_text()
        assert (
            expected in actual_text
        ), f"Текст '{expected}' не найден в '{actual_text}'"
        return self

    def should_be_visible(
        self,
    ):
        element = self.get_element()
        assert element.is_displayed()

    def get_text(self):
        element = self.get_element()
        return element.text

    def should_be_not_visible(self, timeout=5):
        return WebDriverWait(self.driver, timeout).until_not(
            EC.element_to_be_clickable(self.selector)
        )

    def is_checked(self):
        element = self.get_element()
        return element.is_selected()

    def check_message(self, message_text, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: any(
                    message_text in elem.text
                    for elem in d.find_elements(
                        By.CSS_SELECTOR, ".oxd-toast-container *"
                    )
                )
            )
            return True
        except:
            raise AssertionError(f"Сообщение '{message_text}' не появилось")

    def send_key(self, value):

        try:
            elem = self.get_element()
        except TimeoutException:
            raise Exception(f"Элемент {self.selector} не найден")

        tag = elem.tag_name.lower()
        input_type = elem.get_attribute("type")

        if tag == "input" and input_type == "file":
            elem.send_keys(value)
            return self

        try:
            file_input = elem.find_element(By.XPATH, ".//input[@type='file']")
        except NoSuchElementException:
            try:
                parent = elem.find_element(By.XPATH, "..")
                file_input = parent.find_element(By.XPATH, ".//input[@type='file']")
            except NoSuchElementException:
                file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")

        self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(value)
        self.driver.execute_script("arguments[0].style.display = 'none';", file_input)
        return self

    def upload_file(self, file_path):

        abs_path = os.path.abspath(file_path)
        return self.send_key(str(abs_path))

    def is_displayed(self):
        element = self.get_element()
        return element.is_displayed()

    def select_from_dropdown(self, dropdown_locator, option_text):

        dropdown = self.get_element(dropdown_locator)
        dropdown.click()

        option = WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"/  /div[contains(@class, 'oxd-select-option') and contains(text()='{option_text}')]",
                )
            )
        )
        option.click()
