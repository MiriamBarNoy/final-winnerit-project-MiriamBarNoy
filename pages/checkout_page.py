import allure
from playwright.sync_api import Page

class CheckOutPage:
#This will map all locators on login page
    def __init__(self, page: Page):
        self.page = page
        self.name_field = self.page.locator("[data-test=\"firstName\"]")
        self.last_name_field = self.page.locator("[data-test=\"lastName\"]")
        self.postal_code_field = self.page.locator("[data-test=\"postalCode\"]")
        self.submit_btn = self.page.locator("[data-test=\"continue\"]")
        self.cancel_btn = self.page.locator("[data-test=\"cancel\"]")
        self.error_msg = self.page.locator("[data-test=\"error\"]")


#Fill form
    def fill_form(self, name, last_name,postal_code):
        with allure.step("fill checkout form:"):
            self.name_field.fill(name)
            self.last_name_field.fill(last_name)
            self.postal_code_field.fill(postal_code)

#Submit action
    def submit(self):
        with allure.step("submit checkout form:"):
           self.submit_btn.click()

#cancel action
    def cancel(self):
        with allure.step("cancel checkout form:"):
           self.cancel_btn.click()

#retreive error on form filling
    def get_error_message(self):
        with allure.step("get error message upon form filling:"):
            return self.error_msg.inner_text()
