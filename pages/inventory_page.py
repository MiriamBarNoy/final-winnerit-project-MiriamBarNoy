from playwright.sync_api import Page

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page

#set a list of all products with the attributes
    def get_all_products(self):
        products = []
        self.page.wait_for_selector("[data-test=\"inventory-item\"]")
        product_elements = self.page.locator("[data-test=\"inventory-item\"]").all()
        for product in product_elements:
            title = product.locator("[data-test=\"inventory-item-name\"]").inner_text()
            description = product.locator("[data-test=\"inventory-item-desc\"]").inner_text()
            price = float(product.locator("[data-test=\"inventory-item-price\"]").inner_text().strip("$"))
            purchase_btn = product.get_by_text("Add to cart")
            products.append({
                "title": title,
                "description": description,
                "price": price,
                "purchase_btn":  purchase_btn
            })

        return products

#enable getting specific product
    def get_product(self, index: int):
        products = self.get_all_products()
        if 0 <= index < len(products):
            return products[index]

#num of item on the cart icon
    def get_items_qty(self):
        items_qty= int(self.page.locator("[data-test=\"shopping-cart-badge\"]").text_content())
        return  items_qty
#adding products action
    def add_to_cart(self,product_index):
        self.get_product(product_index)["purchase_btn"].click()

#click on cart to move to cart page
    def click_cart(self):
        self.page.locator("[data-test=\"shopping-cart-link\"]").click()


