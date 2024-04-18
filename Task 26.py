import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IMDBSearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_input = (By.ID, 'search_name')
        self.title_type_dropdown = (By.ID, 'search_type')
        self.search_button = (By.XPATH, '//button[@class="primary btn"]')

    def search(self, name, title_type):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.name_input)).send_keys(name)
        self.driver.find_element(*self.title_type_dropdown).send_keys(title_type)
        self.driver.find_element(*self.search_button).click()


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.mark.parametrize("name, title_type", [
    ("Tom Cruise", "Movies"),
    ("Johnny Depp", "TV Episodes"),
    ("Angelina Jolie", "Celebs"),
])
def test_imdb_search(driver, name, title_type):
    driver.get("https://www.imdb.com/search/name/")
    search_page = IMDBSearchPage(driver)
    search_page.search(name, title_type)

    # Verify search results
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'main')))
    assert "No results found." not in driver.page_source, "No results found for '{}' with title type '{}'.".format(name, title_type)


if __name__ == "__main__":
    pytest.main(["-v"])
