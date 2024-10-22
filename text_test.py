from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from PIL import Image
import cv2
import requests
import pytesseract
import time
import os
import base64
from helium import click


options = uc.ChromeOptions()

options.add_argument("--start-maximized")  # 放大視窗

driver = uc.Chrome(options=options)

# 打开 TixCraft 网站
driver.get("https://tixcraft.com/ticket/ticket/24_colde/17640/2/47")

def buy_page():
    #選擇票數
    elem_select_num = driver.find_element("css selector", "select.form-select.mobile-select")
    Select(elem_select_num).select_by_value("4")

    #點掉cookie
    cookies = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    cookies.click()

def send_image():
    # 設定儲存圖片的目錄
    output_dir = 'captcha'
    os.makedirs(output_dir, exist_ok=True)  # 確保目錄存在

    # 用截圖大法取得驗證碼圖片
    img_base64 = driver.execute_script("""
            var ele = arguments[0];
            var cnv = document.createElement('canvas');
            cnv.width = ele.width; cnv.height = ele.height;
            cnv.getContext('2d').drawImage(ele, 0, 0);
            return cnv.toDataURL('image/jpeg').substring(22);    
        """, driver.find_element(By.XPATH, "//*[@id='TicketForm_verifyCode-image']"))

    # 儲存圖片為 PNG 格式
    with open("captcha_login.png", 'wb') as image:
        image.write(base64.b64decode(img_base64))

    # 讀取圖片並進行預處理
    img = cv2.imread('captcha_login.png')
    imginfo = img.shape  # 獲取圖片尺寸 (高度, 寬度)

    # 將彩色圖片轉為灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 計算圖片中心並進行旋轉
    height, width = imginfo[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, -5, 1.0)  # 順時針旋轉 5 度
    gray1 = cv2.warpAffine(gray, M, (width, height))

    # 顏色反轉
    dst = 255 - gray1

    # 儲存處理後的灰階圖片
    cv2.imwrite(os.path.join(output_dir, 'captcha_gray.png'), dst)

    # 進行圖片二元化
    picture = Image.open(os.path.join(output_dir, 'captcha_gray.png')).convert('L')
    threshold = 115

    # 構建二元化的轉換表
    table = [0 if i < threshold else 1 for i in range(256)]
    binary = picture.point(table, '1')
    binary.save(os.path.join(output_dir, 'captcha_binary.png'))

    # 圖片識別
    Pic_read = Image.open(os.path.join(output_dir, 'captcha_binary.png'))
    text = pytesseract.image_to_string(Pic_read)

    time.sleep(1)
    # 輸入驗證碼
    input_captcha = driver.find_element(By.CSS_SELECTOR, "input.greyInput")
    input_captcha.send_keys(text)

    try:
        driver.switch_to.alert.accept()  # 若出現彈出視窗，點掉
    except Exception:
        # 輸入驗證碼
        input_captcha = driver.find_element(By.CSS_SELECTOR, "input.greyInput")
        input_captcha.send_keys(text)
        options.set_capability("unhandledPromptBehavior","accept")
        pass

def accept_submit():
    # 點選"我同意"
    accept = driver.find_element(By.CSS_SELECTOR,"input.form-check-input")
    accept.click()

    #送出按鈕
    submit = driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary.btn-green")
    submit.click()

# def if_error_next():


if __name__ == "__main__" :
    buy_page()
    send_image()
    accept_submit()
    input("Press Enter to close")


