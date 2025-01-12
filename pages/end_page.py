import allure
from playwright.sync_api import Page

class EndPage:
#This will map all locators on end page
    def __init__(self, page: Page):
        self.page = page
        self.complete_header = self.page.locator("[data-test=\"complete-header\"]")
        self.complete_text = self.page.locator("[data-test=\"complete-text\"]")
        self.back_btn = self.page.locator("[data-test=\"back-to-products\"]")

 #header retrieve
    def get_header(self):
        with allure.step("get end page header:"):
            return self.complete_header.inner_text()
#message retrieve
    def get_text_msg(self):
        with allure.step("get end page message:"):
           return self.complete_text.inner_text()

 #go back action
    def go_back(self):
        with allure.step("go back on end page:"):
            self.back_btn.click()
