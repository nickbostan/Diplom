import re

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Diplom.core.base_element import BaseElement


class ColorPicker:
    def __init__(self, driver, preview_locator):
        self.driver = driver
        self.preview_locator = preview_locator
        self.hex_input_locator = (By.CSS_SELECTOR, "div.oxd-color-picker input.oxd-input")
        self.picker_panel_locator = (By.CSS_SELECTOR, "div.oxd-color-picker")

    def select_color_by_hex(self, hex_color: str):
        try:
            preview = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.preview_locator)
            )
            preview.click()
        except ElementClickInterceptedException:
            preview = self.driver.find_element(*self.preview_locator)
            self.driver.execute_script("arguments[0].click();", preview)

        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.hex_input_locator)
        )

        hex_element = BaseElement(self.driver, self.hex_input_locator)
        hex_element.fill(hex_color)  # ввод с '#'
        hex_element.get_element().send_keys("\ue007")  # Enter

        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(self.picker_panel_locator)
        )
        return self

    def get_selected_color(self) -> str:
        preview = self.driver.find_element(*self.preview_locator)
        bg_color = preview.value_of_css_property("background-color")
        return self._rgb_to_hex(bg_color)

    def get_selected_rgb(self) -> tuple:
        preview = self.driver.find_element(*self.preview_locator)
        bg_color = preview.value_of_css_property("background-color")
        match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', bg_color)
        if match:
            return tuple(map(int, match.groups()))
        return 0, 0, 0



    def has_error(self, timeout=2):
        try:
            error_element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "oxd-input-field-error-message"))
            )
            return error_element.is_displayed()
        except:
            return False

    @staticmethod
    def _rgb_to_hex(rgb_string: str) -> str:
        match = re.search(r'(\d+),\s*(\d+),\s*(\d+)', rgb_string)
        if match:
            r, g, b = map(int, match.groups())
            return f"#{r:02x}{g:02x}{b:02x}".upper()
        return rgb_string