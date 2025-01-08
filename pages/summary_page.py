from playwright.sync_api import Page

class SummaryPage:
    def __init__(self, page: Page):
        self.page = page

    # set a list of all purchased items
    def get_all_purchased(self):
        products = []
        self.page.wait_for_selector("[data-test=\"inventory-item\"]")
        product_elements = self.page.locator("[data-test=\"inventory-item\"]").all()
        for product in product_elements:
            title = product.locator("[data-test=\"inventory-item-name\"]").inner_text()
            description = product.locator("[data-test=\"inventory-item-desc\"]").inner_text()
            price = float(product.locator("[data-test=\"inventory-item-price\"]").inner_text().strip("$"))
            item_quantity = int(product.locator("[data-test=\"item-quantity\"]").inner_text())
            products.append({
                "title": title,
                "description": description,
                "price": price,
                "item_quantity": item_quantity
            })

        return products

    # enable getting specific product by index
    def get_cart_product(self, index: int):
        products = self.get_all_purchased()
        if 0 <= index < len(products):
            return products[index]

    def get_payment_method(self):
        payment_method = self.page.locator("data-test=\"payment-info-value\"").inner_text()
        return payment_method

    def get_subtotal(self):
        subtotal = float(self.page.locator("[data-test=\"subtotal-label\"]").inner_text().strip("Item total: $"))
        return subtotal

    def get_tax_value(self):
        tax_value = float(self.page.locator("[data-test=\"tax-label\"]").inner_text().strip("Tax: $"))
        return tax_value

    def get_total(self):
        total = float(self.page.locator("[data-test=\"total-label\"]").inner_text().strip("Total: $"))
        return total

    #cancel action
    def cancel(self):
        cancel_btn = self.page.locator("#cancel")
        cancel_btn.click()

    def finish(self):
        finish_btn = self.page.locator("#finish")
        finish_btn.click()