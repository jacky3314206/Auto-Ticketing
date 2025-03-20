import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

@pytest.fixture
def driver():
    """ 每個測試案例會建立並關閉一個新的 WebDriver 實例 """
    options = Options()
    options.add_argument("--headless")  # CI/CD 不會開瀏覽器視窗
    options.add_argument("--start-maximized")
    _driver = Chrome(options)
    yield _driver
    _driver.quit()

def test_login_page(driver):
    """ 測試是否成功打開 Leetcode 登入頁面 """
    url = "https://leetcode.com/accounts/login/"
    driver.get(url)

    # 檢查頁面標題是否包含 "LeetCode"
    assert "LeetCode" in driver.title

def test_login_form(driver):
    """ 測試登入表單是否存在 """
    url = "https://leetcode.com/accounts/login/"
    driver.get(url)

    # 等待表單出現
    form = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//form[@class='form__2-sN']"))
    )
    assert form is not None

    # 測試登入框是否存在
    login_input = driver.find_element(By.XPATH, "//form[@class='form__2-sN']/span[1]/input")
    assert login_input.get_attribute("type") == "text"

    # 測試密碼框是否存在
    pwd_input = driver.find_element(By.XPATH, "//form[@class='form__2-sN']/span[2]/input")
    assert pwd_input.get_attribute("type") == "password"
