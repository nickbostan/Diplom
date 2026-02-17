from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("button[type='submit']")
        self.error_alert = page.locator(".oxd-alert-content")
        self.empty_error = page.locator(".oxd-input-field-error-message")

    def open(self):
        self.page.goto(
            "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
        )

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        # Дожидаемся окончания редиректа (например, появления Dashboard)
        self.page.wait_for_url("**/dashboard/index**", timeout=10000)
        return self

    def should_be_opened(self):
        expect(self.page).to_have_url("**/auth/login**")
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    def get_error_text(self):
        return self.error_alert.text_content()
