from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page

    # set a list of all products in cart with the attributes
    def get_all_cart_products(self):
        products = []
        self.page.wait_for_selector("[data-test=\"inventory-item\"]")
        product_elements = self.page.locator("[data-test=\"inventory-item\"]").all()
        for product in product_elements:
            title = product.locator("[data-test=\"inventory-item-name\"]").inner_text()
            description = product.locator("[data-test=\"inventory-item-desc\"]").inner_text()
            price = float(product.locator("[data-test=\"inventory-item-price\"]").inner_text().strip("$"))
            remove_btn = product.get_by_text("Remove")
            item_quantity = int(product.locator("[data-test=\"item-quantity\"]").inner_text())
            products.append({
                "title": title,
                "description": description,
                "price": price,
                "remove_btn":  remove_btn,
                "item_quantity": item_quantity
            })

        return products

    # enable getting specific product by index
    def get_cart_product(self, index: int):
        products = self.get_all_cart_products()
        if 0 <= index < len(products):
            return products[index]

#remove from cart action
    def remove_from_cart(self,product_index):
        self.get_cart_product(product_index)["remove_btn"].click()

#checkout action
    def checkout(self):
        checkout_btn = self.page.locator("#checkout")
        checkout_btn.click()

#continue shopping action
    def continue_shopping(self):
        continue_btn = self.page.locator("#continue-shopping")
        continue_btn.click()