from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time

class LoginPage:

    BUTTON_USER_ACCOUNT = (By.XPATH, '(//*[@class="header-action-button"])[1]')
    EMAIL_FIELD = (By.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[type="password"]')
    CONNECT_BUTTON = (By.XPATH, '//button[contains(., "Conectează-te")]')
    VERIFY_LOGIN = (By.XPATH, '//span[contains(text(), "Contul meu")]')
    TEXT_CHECKBOX = (By.ID, "NCxXf2")
    CHECKBOX = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    BUTTON_ACCEPT_COOKIES = (By.CSS_SELECTOR, 'button[data-test-id="customer-consents-button"]') 

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5) 

    def navigate_to_login(self):
        try:
            cookie_button = self.wait.until(EC.element_to_be_clickable(self.BUTTON_ACCEPT_COOKIES))
            cookie_button.click()
            print("Cookie banner acceptat. Se continuă spre login.")
        except:
            print("Nu a fost detectat niciun banner de cookie-uri sau pop-up.")
            pass
            
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_USER_ACCOUNT))
        self.driver.find_element(*self.BUTTON_USER_ACCOUNT).click()
        
        try:
            self.wait.until(EC.element_to_be_clickable(self.EMAIL_FIELD))
        except:
            print("Câmpul de login nu a apărut la timp.")
            pass

    def fill_and_submit_login(self, email, password):
        self.wait.until(EC.element_to_be_clickable(self.EMAIL_FIELD))
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
    
    def click_login_button(self):
        self.wait.until(EC.element_to_be_clickable(self.CONNECT_BUTTON))
        self.driver.find_element(*self.CONNECT_BUTTON).click()

    def is_login_successful(self):
        self.wait.until(EC.visibility_of_element_located(self.VERIFY_LOGIN))


@given("Utilizatorul acceseaza siteul")
def step_enter_site(context):
    
    options = Options()
    options.page_load_strategy = "eager"

    context.driver = uc.Chrome(headless=False, options=options)
    
    context.driver.maximize_window()
    context.driver.get("https://epantofi.ro/")

    context.login_page = LoginPage(context.driver)

@then("Utilizatorul da click pe butonul de login")
def step_click_login_button(context):
    context.login_page.navigate_to_login()

@then('Introduce credentialele: email "{email}" si parola "{password}"')
def step_introduce_creds(context, email, password):
    context.login_page.fill_and_submit_login(email, password)

@when("Apasa pe butonul de conectare")
def step_press_login_button(context):
    context.login_page.click_login_button()

@then("Loginul a reusit")
def step_login_complete(context):
    context.login_page.is_login_successful()
    context.driver.quit()