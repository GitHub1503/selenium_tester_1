import pytest
import uuid
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(autouse=True)
def driver():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    #driver.get('https://petfriends.skillfactory.ru')
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Вернуть объект браузера
    yield browser

    # Этот код выполнится после отрабатывания теста:
    try:
        browser.execute_script("document.body.bgColor = 'red';")

        #Сделать скриншот:
        browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

        #Вывести логи:
        print('URL: ', browser.current_url)
        print('Browser logs:')
        for log in browser.get_log('browser'):
            print(log)

    except:
        pass  # just ignore any errors here



