from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

class SearchItem:

    BUTTON_ACCEPT_COOKIES = (By.CSS_SELECTOR, 'button[data-test-id="customer-consents-button"]') 
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'input[id="search-input-field-header-id"]')

    COLOUR_FILTER = (By.XPATH, '//button[contains(., "Culoare")]')
    BUTTON_CHECK_MENU = (By.CSS_SELECTOR, 'button[class="button-icon back s tertiary"]')
    APPLY_FILTER_BUTTON = (By.XPATH, '//button[contains(., "Afișează")]')
    CHECK_COLOUR_FILTER = (By.XPATH, '//button[contains(., "Culoare")]//span[contains(@class, "circle-digit indicator primary")]')

    SIZE_FILTER = (By.XPATH, '//button[contains(., "Mărime")]')
    #same APPLY_FILTER_BUTTON
    CHECK_SIZE_FILTER = (By.XPATH, '//button[contains(., "Mărime")]//span[contains(@class, "circle-digit indicator primary")]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    def click_search_bar(self):
        try:
            cookie_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_ACCEPT_COOKIES))
            cookie_button.click()
            print("Cookie acceptat.")
        except:
            print("Cookie banner inexistent")
        
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))

    def fill_search_bar(self, text):
        search_input = self.driver.find_element(*self.SEARCH_BUTTON)
        search_input.send_keys(text + Keys.ENTER)
    
    def choose_colour(self, colour):
        self.wait.until(EC.element_to_be_clickable(self.COLOUR_FILTER)).click()

        colour_path = (By.XPATH, f'//label[.//span[contains(text(), "{colour}")]]')

        try:
            self.wait.until(EC.element_to_be_clickable(colour_path)).click()
            print(f"Color '{colour}' selected successfully")
        except:
            print(f"Error: Color '{colour}' was not found")
            raise ValueError("Color was not found")
        
        try:
            self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTER_BUTTON)).click()
        except:
            print("Error: The 'Show' button could not be accessed.")

        try:
            self.wait.until(EC.presence_of_element_located(self.CHECK_COLOUR_FILTER))
            print("Color filter applied.")
        except:
            print("Error: Color filter not applied.")

    def choose_size(self, size):
        self.wait.until(EC.element_to_be_clickable(self.SIZE_FILTER)).click()

        size_path = (By.XPATH, f'//div[contains(@class, "pill-size basic") and .//span[contains(text(), "{size}")]]')
        
        try:
            self.wait.until(EC.element_to_be_clickable(size_path)).click()
            print(f"Size '{size}' selected successfully")
        except:
            print(f"Error: Size '{size}' was not found")
            raise ValueError("Size was not found")
            
        try:
            self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTER_BUTTON)).click()
        except:
            print("Error: The 'Show' button could not be accessed.")

        try:
            self.wait.until(EC.presence_of_element_located(self.CHECK_SIZE_FILTER))
            print("Size filter applied.")
        except:
            print("Error: Size filter not applied.")
    
@given("The user is on the site")
def step_enter_site(context):
    options = Options()
    options.page_load_strategy = "eager"

    context.driver = uc.Chrome(options=options)

    context.driver.maximize_window()
    context.driver.get("https://epantofi.ro/")

    context.search_test = SearchItem(context.driver)

@then("The user clicks the search bar")
def step_click_searchbar(context):
    context.search_test.click_search_bar()

@then('The user enters the name of a footwear item "{name}"')
def step_introduce_text(context, name):
    context.search_test.fill_search_bar(name)

@then('The user selects a "{color}"')
def step_select_colour(context, color):
    context.search_test.choose_colour(color)

@then('The user selects a specific "{size}"')
def step_select_size(context, size):
    context.search_test.choose_size(size)
    context.driver.quit()