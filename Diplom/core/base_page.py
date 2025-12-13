from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self, url):
        self.driver.get(url)

    def page_should_be_opened(self, expected_url, title=None):
        assert self.wait.until(EC.url_contains(expected_url))

        if title:
            assert self.wait.until(EC.title_contains(title))

    def click_new_page(self, new_url):
        original_url = self.driver.current_url
        self.driver.get(new_url)
        self.wait.until(EC.url_changes(original_url))

    def wait_for_windows_count(self, expected_count):
        self.wait.until(EC.number_of_windows_to_be(expected_count))

    def switch_to_new_window(self, expected_windows=2):
        original_window = self.driver.current_window_handle
        original_url = self.driver.current_url

        self.wait_for_windows_count(expected_windows)

        for window in self.driver.window_handles:
            if window != original_window:
                self.driver.switch_to.window(window)
                break

        new_url = self.driver.current_url
        assert new_url != original_url
        return new_url

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()

