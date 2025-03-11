from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


class Car_valuation_page:

    def __init__(self, driver):
        self.driver = driver
        self.reg_input = (By.ID, 'subForm1')
        self.submit = (By.XPATH, "//button[@type='submit']")
        self.notification = (By.CSS_SELECTOR, '.alert.alert-danger')
        self.make = (By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                               "'Make')]/following-sibling::td")
        self.model = (By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                "'Model')]/following-sibling::td")
        self.year = (By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                               "'Year')]/following-sibling::td")

    def launch_site(self, url):
        self.driver.get(url)

    def reg_number(self, vehicle_reg):
        self.driver.find_element(*self.reg_input).send_keys(vehicle_reg)
        self.driver.find_element(*self.submit).click()

    def is_notification_displayed(self):
        len(self.driver.find_elements(*self.notification)) > 0

    def get_vehicle_details(self):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".general-information")))
        make = self.driver.find_element(*self.make).text
        model = self.driver.find_element(*self.model).text
        year = self.driver.find_element(*self.year).text
        print('Make : ' + make + ' Model : ' + model + ' Year : ' + year)
        return make, model, year
