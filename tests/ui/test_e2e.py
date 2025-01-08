import pytest
from assertpy import assert_that
from faker.contrib.pytest.plugin import faker
from faker.proxy import Faker
from playwright.sync_api import sync_playwright, Browser, expect
from tests.conftest import base_url_ui
from tests.conftest import setup_browser
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.checkout_page import CheckOutPage
from pages.end_page import EndPage
from pages.summary_page import SummaryPage

#this will test sanity E2E
def test_sanity_e2e_flow(setup_browser,base_url_ui):
    this_page = setup_browser
    login_page = LoginPage(this_page)
    inventory_page = InventoryPage(this_page)
    cart_page = CartPage(this_page)
    checkout_page = CheckOutPage(this_page)
    summary_page = SummaryPage(this_page)
    end_page = EndPage(this_page)
#login
    login_page.login("standard_user", "secret_sauce")
#add items - and keep their properties for further assertion
    inventory_page.add_to_cart(0)
    first_item_title = inventory_page.get_product(0)["title"]
    first_item_desc = inventory_page.get_product(0)["description"]
    first_item_price = inventory_page.get_product(0)["price"]
    inventory_page.add_to_cart(5)
    second_item_title = inventory_page.get_product(5)["title"]
    second_item_desc = inventory_page.get_product(5)["description"]
    second_item_price = inventory_page.get_product(5)["price"]
#assert correct item quantity
    assert inventory_page.get_items_qty() == 2
    inventory_page.click_cart()
    assert this_page.url == f'{base_url_ui}cart.html'
#assert correct items on cart
    cart_first_item = cart_page.get_cart_product(0)
    cart_second_item = cart_page.get_cart_product(1)
    assert len(cart_page.get_all_cart_products()) == 2
    assert first_item_title == cart_first_item["title"]
    assert second_item_title == cart_second_item["title"]
    assert first_item_price == cart_first_item["price"]
    assert second_item_price == cart_second_item["price"]
    assert first_item_desc == cart_first_item["description"]
    assert second_item_desc == cart_second_item["description"]
    assert cart_second_item["item_quantity"] == 1
    assert cart_first_item["item_quantity"] == 1
#checkout
    cart_page.checkout()
    assert this_page.url == f'{base_url_ui}checkout-step-one.html'
#fill form with fake first, last name & pb code and submit
    checkout_page.fill_form(Faker().first_name(),Faker().last_name(),Faker().postcode())
    checkout_page.submit()
    assert this_page.url == f'{base_url_ui}checkout-step-two.html'
#assert correct items on final summary page
    summary_first_item = summary_page.get_cart_product(0)
    summary_second_item =summary_page.get_cart_product(1)
    assert len(cart_page.get_all_cart_products()) == 2
    assert first_item_title == summary_first_item["title"]
    assert second_item_title == summary_second_item["title"]
#assert correct total price & taxes
    subtotal = summary_page.get_subtotal()
    taxes = summary_page.get_tax_value()
    total = summary_page.get_total()
    assert subtotal == (summary_first_item["price"] + summary_second_item["price"])
    assert taxes == round((subtotal*0.08),2)
    assert total == round((subtotal + taxes),2)
#finish
    summary_page.finish()
    assert this_page.url == f'{base_url_ui}checkout-complete.html'
#assert the end page
    assert end_page.get_header() == "Thank you for your order!"
    assert end_page.get_text_msg() == "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
    end_page.go_back()
#assert that when finish we get back to inventory
    assert this_page.url == f'{base_url_ui}inventory.html'

#this will test remove item E2E
def test_remove_item_e2e_flow(setup_browser,base_url_ui):
    this_page = setup_browser
    login_page = LoginPage(this_page)
    inventory_page = InventoryPage(this_page)
    cart_page = CartPage(this_page)
    checkout_page = CheckOutPage(this_page)
    summary_page = SummaryPage(this_page)
#login
    login_page.login("standard_user", "secret_sauce")
#add items
    inventory_page.add_to_cart(0)
    inventory_page.add_to_cart(5)
    inventory_page.add_to_cart(3)
    inventory_page.add_to_cart(4)
#assert correct item quantity
    assert inventory_page.get_items_qty() == 4
    inventory_page.click_cart()
#remove to items & assert updated
    assert len(cart_page.get_all_cart_products()) == 4
    cart_page.remove_from_cart(0)
    cart_page.remove_from_cart(1)
    assert len(cart_page.get_all_cart_products()) == 2
#checkout
    cart_page.checkout()
    assert this_page.url == f'{base_url_ui}checkout-step-one.html'
#fill form with fake first, last name & pb code and submit
    checkout_page.fill_form(Faker().first_name(),Faker().last_name(),Faker().postcode())
    checkout_page.submit()
    assert this_page.url == f'{base_url_ui}checkout-step-two.html'
#assert correct items on final summary page
    summary_first_item = summary_page.get_cart_product(0)
    summary_second_item =summary_page.get_cart_product(1)
    assert len(cart_page.get_all_cart_products()) == 2
#assert correct total price & taxes
    subtotal = summary_page.get_subtotal()
    taxes = summary_page.get_tax_value()
    total = summary_page.get_total()
    assert subtotal == (summary_first_item["price"] + summary_second_item["price"])
    assert taxes == round((subtotal*0.08),2)
    assert total == round((subtotal + taxes),2)
#finish
    summary_page.finish()
    assert this_page.url == f'{base_url_ui}checkout-complete.html'

