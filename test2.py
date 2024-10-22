import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def make_webdriver() -> Chrome:
    options = create_options()
    driver = Chrome(options)

    return driver

def create_options() -> Options:
    options = Options()
    # options.add_argument("--headless") #讓瀏覽器進入無頭模式，簡單來說就是放在背景運行，不會實際開一個視窗出來
    options.add_argument("--start-maximized") #確保瀏覽器每次執行時都可以開到最大的視窗，避免 RWD 造成一些元素讀不到

    return options


def demo_css_selector():
    # 回傳最先找到的元素，若沒有找到則會跳 error
    data = _driver.find_element(By.CSS_SELECTOR, "div.b-ent").text
    print(data)

    # 會尋找目前葉面當中所有符合條件的元素，並回傳一個 list，若沒找到會回傳一個空 list
    datas = _driver.find_elements(By.CSS_SELECTOR, "div.b-ent")
    [print(tmp.text) for tmp in datas]

def demo_wait():
    # 單個元素，回傳 webelement 物件
    data = WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "ul.tag-cloud")))
    print(data.text)

    # 多個元素，回傳 list
    datas = WebDriverWait(_driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.tag-cloud")))
    [print(tmp.text) for tmp in datas]
def demo_xpath():
    time.sleep(10)
    form = _driver.find_element(By.XPATH,"//form[@class='form__2-sN']")
    print(form.get_attribute("type"))
    login = _driver.find_element(By.XPATH,"//form[@class='form__2-sN']/span[1]/input")
    print(login.get_attribute("type"))
    pwd = _driver.find_element(By.XPATH,"//form[@class='form__2-sN']/span[2]/input")
    print(login.get_attribute("type"))

if __name__ == '__main__':
    url = "https://leetcode.com/accounts/login/"
    _driver = make_webdriver()

    _driver.get(url=url)

    demo_xpath()
