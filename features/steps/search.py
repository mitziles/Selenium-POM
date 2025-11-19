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
            print(f"Culoare '{colour}' aleasa cu succes")
        except:
            print(f"Eroare: Culoarea '{colour}' nu a fost gasita")
            raise ValueError("Culoarea nu a fost gasita")
        
        try:
            self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTER_BUTTON)).click()
        except:
            print("Eroare: Butonul 'Afișează' nu a putut fi accesat.")

        try:
            self.wait.until(EC.presence_of_element_located(self.CHECK_COLOUR_FILTER))
            print("Filtru de culoare aplicat.")
        except:
            print("Eroare: Filtru de culoare neaplicat.")

    def choose_size(self, size):
        self.wait.until(EC.element_to_be_clickable(self.SIZE_FILTER)).click()

        size_path = (By.XPATH, f'//div[contains(@class, "pill-size basic") and .//span[contains(text(), "{size}")]]')
        
        try:
            self.wait.until(EC.element_to_be_clickable(size_path)).click()
            print(f"Marime '{size}' aleasa cu succes")
        except:
            print(f"Eroare: Marimea '{size}' nu a fost gasita")
            raise ValueError("Marimea nu a fost gasita")
            
        try:
            self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTER_BUTTON)).click()
        except:
            print("Eroare: Butonul 'Afișează' nu a putut fi accesat.")

        try:
            self.wait.until(EC.presence_of_element_located(self.CHECK_SIZE_FILTER))
            print("Filtru de marime aplicat.")
        except:
            print("Eroare: Filtru de marime neaplicat.")
    
@given("Userul intra pe site")
def step_enter_site(context):
    options = Options()
    options.page_load_strategy = "eager"

    context.driver = uc.Chrome(options=options)

    context.driver.maximize_window()
    context.driver.get("https://epantofi.ro/")

    context.search_test = SearchItem(context.driver)

@then("Userul da click pe search bar")
def step_click_searchbar(context):
    context.search_test.click_search_bar()

@then('Userul introduce numele unei perechi de incaltaminte "{nume}"')
def step_introduce_text(context, nume):
    context.search_test.fill_search_bar(nume)

@then('Userul alege o "{culoare}"')
def step_select_colour(context, culoare):
    context.search_test.choose_colour(culoare)

@then('Userul alege o anumite "{marime}"')
def step_select_size(context, marime):
    context.search_test.choose_size(marime)
    context.driver.quit()