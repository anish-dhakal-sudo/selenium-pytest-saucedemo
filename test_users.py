import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()

@pytest.fixture(scope="session")
def logged_in_driver():
    """Logs in once and provides a driver with an active session for all tests."""
    driver = webdriver.Chrome(service=Service(executable_path="../chromedriver.exe"))  # Initialize WebDriver

    # Navigate to login page
    driver.get('https://www.saucedemo.com/')

    # Find and clear input fields before entering credentials
    username_input = driver.find_element(By.ID, "user-name")
    username_input.clear()
    username_input.send_keys("standard_user")

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("secret_sauce")

    # Click login button
    driver.find_element(By.ID, "login-button").click()

    time.sleep(2)  # Wait for page to load
    assert "inventory.html" in driver.current_url, "Login unsuccessful"

    yield driver  # Provide the driver instance to all tests

    driver.quit()  # Cleanup after all tests finish


@pytest.mark.skip(reason="no way of currently testing this")
def test_google(driver):
    """Example test for visiting Google."""
    driver.get('https://www.google.com')
    time.sleep(10)


def test_saucedemo(logged_in_driver):
    """Verifies successful login."""
    assert "inventory.html" in logged_in_driver.current_url
    print("Login successful!")

@pytest.mark.skip(reason="no way of currently testing this")
def test_cart(logged_in_driver):
    """Uses the logged-in session and adds a specific item to the cart."""

    # Find and click 'Add to Cart' for a specific item
    item_id = "add-to-cart-sauce-labs-backpack"
    add_to_cart_button = logged_in_driver.find_element(By.ID, item_id)
    add_to_cart_button.click()

    time.sleep(2)  # Wait for item to be added

    # Verify item is added by checking if the button changed to 'Remove'
    remove_button = logged_in_driver.find_element(By.ID, "remove-sauce-labs-backpack")
    assert remove_button.is_displayed(), "Item was not added to the cart"

    print("Item successfully added to the cart!")


def test_add_multiple_items_to_cart(logged_in_driver):
    """Add multiple items to the cart and verify they are present."""

    item_ids = [
        "add-to-cart-sauce-labs-backpack",
        "add-to-cart-sauce-labs-bike-light",
        "add-to-cart-sauce-labs-bolt-t-shirt"
    ]

    wait = WebDriverWait(logged_in_driver, 10)

    # Add each item and confirm it's added
    for item_id in item_ids:
        add_button = wait.until(EC.element_to_be_clickable((By.ID, item_id)))
        add_button.click()

        # Confirm the button changed to "Remove"
        remove_id = item_id.replace("add-to-cart-", "remove-")
        wait.until(EC.presence_of_element_located((By.ID, remove_id)))

    # Go to cart
    cart_button = wait.until(EC.element_to_be_clickable((By.ID, "shopping_cart_container")))
    cart_button.click()

    # Confirm cart page loaded
    wait.until(EC.url_contains("cart.html"))

    # Wait for all 3 items to appear
    wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "cart_item")) >= 3)

    # Final verification
    for item_id in item_ids:
        remove_id = item_id.replace("add-to-cart-", "remove-")
        assert logged_in_driver.find_element(By.ID, remove_id).is_displayed(), f"{remove_id} not found"

    print("✅ All selected items successfully added to the cart!")
