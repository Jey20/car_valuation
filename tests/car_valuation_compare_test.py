import pytest

from file_utils import File_utils
from selenium import webdriver
from pages.car_valuation_page import Car_valuation_page
from selenium.webdriver.common.by import By
import time


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager.install()))
    yield driver
    driver.close()
    driver.quit()


def get_vehicle_details_from_valuation_site(driver, vehicle_reg):
    print("reg : " + vehicle_reg)

    car_valuation_page = Car_valuation_page(driver)
    car_valuation_page.launch_site("https://car-checking.com/")
    car_valuation_page.reg_number(vehicle_reg)

    time.sleep(1)

    if len(driver.find_elements(By.CSS_SELECTOR, '.alert.alert-danger')) > 0:
        print("The license plate number is not recognised")
        return ()

    car_details = car_valuation_page.get_vehicle_details()
    return car_details


def test_car_valuation_compare(driver):
    registrations = File_utils.get_registration_numbers_from_input_file()
    print(registrations)

    car_output_dict = File_utils.get_details_from_output_file()
    print(car_output_dict)

    for reg in registrations:
        car_detail_tuple = get_vehicle_details_from_valuation_site(driver, reg)
        if len(car_detail_tuple) > 0:
            assert ','.join(car_detail_tuple) == car_output_dict.get(reg)
        else:
            print(reg + ' is not a valid vehicle registration number ')
