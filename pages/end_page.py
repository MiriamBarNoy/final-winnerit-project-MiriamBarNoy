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
        return self.complete_header.inner_text()
#message retrieve
    def get_text_msg(self):
        return self.complete_text.inner_text()

 #go back action
    def go_back(self):
        self.back_btn.click()
