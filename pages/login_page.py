from playwright.sync_api import Page

class LoginPage:
#This will map all locators on login page
    def __init__(self, page: Page):
        self.page = page
        self.user_field = self.page.locator("[data-test=\"username\"]")
        self.password_field = self.page.locator("[data-test=\"password\"]")
        self.submit_btn = self.page.locator("[data-test=\"login-button\"]")
        self.error = self.page.locator("[data-test=\"error\"]")

#Login action
    def login(self, username, password):
        self.user_field.fill(username)
        self.password_field.fill(password)
        self.submit_btn.click()

#retreive error login message
    def get_error_message(self):
        return self.error
