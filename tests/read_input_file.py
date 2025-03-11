from functools import reduce

import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import time

from file_utils import File_utils


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager.install()))
    yield driver
    driver.close()
    driver.quit()


def test_output_file():
    output_dict = {}
    out_file_path = '../car_output - V6.txt'

    with open(out_file_path, 'r') as f:
        next(f)
        for line in f:
            values = line.split(',', maxsplit=1)
            key = values[0]
            val = (values[1].rstrip('\n'))
            output_dict[key] = val
        print(output_dict)


def get_registration_numbers_from_input_file():
    file_path = '../car_input - V6.txt'
    pattern = r'\b[A-Z]{2}\d{2}[A-Z]{3}\b|\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b'
    registrations = []
    with open(file_path, 'r') as f:
        for line in f:
            registration_numbers = re.findall(pattern, line)
            for reg in registration_numbers:
                registrations.append(reg)

    return registrations


def get_vehicle_details_from_valuation_site(driver, vehicle_reg):
    print("reg : " + vehicle_reg)
    driver.get("https://car-checking.com/")
    # WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "subForm1")))
    reg_number_input = driver.find_element(By.ID, 'subForm1')
    reg_number_input.send_keys(vehicle_reg)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    if len(driver.find_elements(By.CSS_SELECTOR, '.alert.alert-danger')) > 0:
        print("The license plate number is not recognised")
        return ()

    make = driver.find_element(By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                         "'Make')]/following-sibling::td").text
    model = driver.find_element(By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                          "'Model')]/following-sibling::td").text
    year = driver.find_element(By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                         "'Year')]/following-sibling::td").text

    print('Make : ' + make + ' Model : ' + model + ' Year : ' + year)
    car_detail_tuple = (make, model, year)
    return car_detail_tuple


def test_car_reg(driver):
    registrations = File_utils.get_registration_numbers_from_input_file()
    print(registrations)

    car_output_dict = File_utils.get_details_from_output_file()
    print(car_output_dict)

    for reg in registrations:
        car_detail_tuple = get_vehicle_details_from_valuation_site(driver, reg)
        if len(car_detail_tuple) > 0:
            assert ','.join(car_detail_tuple) == car_output_dict.get(reg)
        else:
            print( reg + ' is not a valid vehicle registration number ')


def test_read_file(driver):
    file_path = '../car_input - V6.txt'
    pattern = r'\b[A-Z]{2}\d{2}[A-Z]{3}\b|\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b'

    registrations = []
    with open(file_path, 'r') as f:
        for line in f:
            registration_numbers = re.findall(pattern, line)
            for reg in registration_numbers:
                registrations.append(reg)

    print(registrations[0])

    print(registrations[0])

    driver.get("https://car-checking.com/")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "subForm1")))
    reg_number_input = driver.find_element(By.ID, 'subForm1')
    reg_number_input.send_keys('AD58 VNF')
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    make = driver.find_element(By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                         "'Make')]/following-sibling::td").text
    model = driver.find_element(By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                          "'Model')]/following-sibling::td").text
    year = driver.find_element(By.XPATH, "//div[@class='general-information']//tbody/tr/td[contains(text(),"
                                         "'Year')]/following-sibling::td").text

    print('Make : ' + make + ' Model : ' + model + ' Year : ' + year)
    car_detail_tuple = (make, model, year)

    output_dict = {}
    out_file_path = '../car_output - V6.txt'
    with open(out_file_path, 'r') as f:
        next(f)
        for line in f:
            values = line.split(',', maxsplit=1)
            key = values[0]
            val = (values[1].rstrip('\n'))
            output_dict[key] = val

    print(car_detail_tuple)
    print(output_dict['AD58 VNF'])
    assert ','.join(car_detail_tuple) == output_dict['AD58 VNF']

    # assert car_detail_tuple == output_dict['AD58 VNF']
