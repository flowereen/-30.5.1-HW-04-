import time
import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()

    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    driver.maximize_window()
    yield driver

    driver.quit()


def test_show_my_pets(driver):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    # Вводим почту
    time.sleep(1)
    driver.find_element(By.ID, 'email').send_keys('allyouneedislove242@gmail.com')
    # Вводим пароль
    time.sleep(1)
    driver.find_element(By.ID, 'pass').send_keys('vWj4kq4!JwbGDxM')
    # Нажимаем на кнопку входа в аккаунт
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Открываем страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, '#navbarNav > ul > li:nth-child(1) > a').click()
    # Проверяем, что мы оказались на странице "Мои питомцы"
    assert WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "flowereen"))

    # Проверяем что список моих питомцев не пуст
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody')
    assert len(all_my_pets) > 0

    # Проверяем,что всех питомцев есть имя, порода и возраст
    names = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[1]')
    species = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[2]')
    ages = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[3]')

    for i in range(len(names)):
        assert names[i].text != ''
        assert species[i].text != ''
        assert ages[i].text != ''

    # Проверяем количество питомцев
    time.sleep(5)
    pets_num = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = driver.find_element(By.XPATH, '//table[@class="table table-hover"]tbody/tr')
    pets_count = pets_count.text
    assert int(pets_num) == len(pets_count)

    # Проверяем, что в списке нет повторяющихся питомцев
    list_data_my_pets = []
    for i in range(len(all_my_pets)):
        list_data = all_my_pets[i].text.split("\n")
        list_data_my_pets.append(list_data[0])
    set_data_my_pets = set(list_data_my_pets)
    assert len(list_data_my_pets) == len(set_data_my_pets)

    # Проверяем, что у всех питомцев разные имена
    all_pets_name = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]')
    list_name_my_pets = []
    for i in range(len(all_pets_name)):
        list_name_my_pets.append(all_pets_name[i].text)
    set_name_my_pets = set(list_name_my_pets)
    assert len(list_name_my_pets) == len(set_name_my_pets)

    # Проверяем, что хотя бы у половины питомцев есть фото
    pytest.driver.implicitly_wait(5)
    pets_images = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//img')
    n = 0
    for i in range(len(pets_images)):
        if pets_images[i].get_attribute('src') != '':
            n += 1
    assert n >= all_my_pets / 2
