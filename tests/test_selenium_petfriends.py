import time
from conftest import driver
from conftest import web_browser
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def test_petfriends(web_browser):
    base_url = "https://petfriends.skillfactory.ru/"
    # Открываем страницу авторизации на сайте:
    #driver = web_browser
    web_browser.get(base_url)

    # Кликаем на кнопку "зарегистрироваться"
    btn_newuser = web_browser.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    #btn_newuser_2 = selenium.find_element(By.TAG_NAME, 'button')
    btn_newuser.click()

    # Переходим по ссылке "у меня уже есть аккаунт"
    btn_exist_acc = web_browser.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # вводим email
    field_email = web_browser.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("gavrilov1979@gmail.com")

    # вводим пароль
    field_pass = web_browser.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("BvC_321-Lkj")

    # Нажимаем не кнопку "войти"
    btn_submit = web_browser.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    assert web_browser.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"


def test_show_all_pets(web_browser):
    base_url = "https://petfriends.skillfactory.ru/"
    # Открываем страницу авторизации на сайте:
    web_browser.get(base_url)
    """Явное ожидание появления элемента 'button' в структуре документа"""
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
    btn_newuser = web_browser.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()
    """Явное ожидаание появления в структуре документа ссылки"""
    WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.LINK_TEXT, u"У меня уже есть аккаунт")))
    # Переходим по ссылке "у меня уже есть аккаунт"
    btn_exist_acc = web_browser.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()
    """Явное ожидание видимости элемента 'button на экране'"""
    WebDriverWait(web_browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    # Вводим email
    web_browser.find_element(By.ID, 'email').send_keys('gavrilov1979@gmail.com')
    # Вводим пароль
    web_browser.find_element(By.ID, 'pass').send_keys('BvC_321-Lkj')
    # Нажимаем на кнопку входа в аккаунт
    web_browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    web_browser.implicitly_wait(3)
    # Проверяем, что мы оказались на главной странице пользователя
    assert web_browser.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = web_browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = web_browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = web_browser.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    count_img = 0
    count_manes = 0
    count_no_descr = 0
    for i in range(len(names)):
        if images[i].get_attribute('src') != '':
            count_img += 1
        if names[i].text != '':
            count_manes += 1
        assert descriptions[i].text != ''

        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        if len(parts[0]) == 0 or len(parts[1]) == 0:
            count_no_descr += 1
    assert count_img > len(names)/5
    assert count_manes > len(names)/2
    assert count_no_descr < (len(names)/100)*10

def test_show_my_pets(web_browser):
    base_url = "https://petfriends.skillfactory.ru/"
    # Открываем страницу авторизации на сайте:
    """Неявное ожидание"""
    web_browser.implicitly_wait(10)
    web_browser.get(base_url)
    btn_newuser = web_browser.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()
    """Неявное ожидание"""
    web_browser.implicitly_wait(10)
    # Переходим по ссылке "у меня уже есть аккаунт"
    btn_exist_acc = web_browser.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()
    web_browser.find_element(By.ID, 'email').send_keys('gavrilov1979@gmail.com')
    # Вводим пароль
    web_browser.find_element(By.ID, 'pass').send_keys('BvC_321-Lkj')
    # Нажимаем на кнопку входа в аккаунт
    web_browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    web_browser.implicitly_wait(10)
    web_browser.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    images = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]//img')
    animal_params = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]//td')
    my_pets = len(animal_params)/4
    param_1 = web_browser.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    param_2 = param_1.text
    param_3 = ''.join(param_2.split('\n'))
    parts = param_3.replace("Друзей", ": Друзей")
    #assert parts[1] == 9
    parts_1 = parts.split(": ")
    assert int(parts_1[1]) == my_pets

    animal_params_t = ''
    #Обрабатываем таблицу с питомцами, удаляем нечитаемые символы, преобразуем в удобный формат
    for i in range(1, len(animal_params)):
        if i % 4 == 0:
            animal_params_t += 'QQ; '
        else:
            animal_params_t += animal_params[i-1].text + '; '
    my_pets_list = animal_params_t.split('QQ; ')
    #Перебираем всех питомцев по очереди, проверяя корректность заполнения полей
    for i in range(len(my_pets_list)):
        assert images[i].get_attribute('src') != ''    #Проверяем наличие картинки
        m_p = my_pets_list[i].split('; ')
        assert m_p[0] != ''                            #Проверяем заполнение поля "Имя"
        assert m_p[1] != ''                            #Проверяем заполнение поля "Порода"
        assert m_p[2] != ''                            #Проверяем заполнение поля "Возраст"
    #assert  animal_params_t == 'Qwerty'
