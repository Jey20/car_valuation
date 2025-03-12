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
    print("Vehicle Registration : " + vehicle_reg)

    car_valuation_page = Car_valuation_page(driver)
    car_valuation_page.launch_site("https://car-checking.com/")
    car_valuation_page.reg_number(vehicle_reg)

    time.sleep(1)

    if len(driver.find_elements(By.CSS_SELECTOR, '.alert.alert-danger')) > 0:
        print(f"The license plate {vehicle_reg} is not recognised")
        return ()

    car_details = car_valuation_page.get_vehicle_details()
    return car_details


def test_car_valuation_compare(driver):
    registrations = File_utils.get_registration_numbers_from_input_file()
    print('\nList of vehicle registrations in given input file : ', registrations)

    car_output_dict = File_utils.get_details_from_output_file()
    for key, value in car_output_dict.items():
        print('Vehicle : ', key, ' details in output file :',  value )

    for reg in registrations:
        car_detail_tuple = get_vehicle_details_from_valuation_site(driver, reg)
        if len(car_detail_tuple) > 0:
            assert ','.join(car_detail_tuple) == car_output_dict.get(reg), reg + ' matches with given output file'
        else:
            assert len(car_detail_tuple) == 0, reg + ' is not a valid vehicle registration number  '
