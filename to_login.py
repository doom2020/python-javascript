import requests
from selenium import webdriver
import random
import time
import re
from lxml import etree
import queue
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import hashlib
import os
from PIL import Image
from selenium.webdriver import ActionChains
import cv2
import numpy as np
from PIL import ImageDraw


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}

source_img_path = "index.png"
filter_img_path = "filter.png"
template_img_path = "template.png"
target_img_path = "target.png"

def loading_page():
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--start-maximized")
    # chrome_option.add_argument('--headless')
    # chrome_option.add_argument('--disable-gpu')
    # proxy = "--proxy-server=http://" + '175.7.199.129:3256'
    user_agent = "user-agent=" + headers['user-agent']
    # chrome_option.add_argument(proxy)
    chrome_option.add_argument(user_agent)
    driver = webdriver.Chrome(chrome_options=chrome_option)
    driver.set_page_load_timeout(random.randint(50, 80))
    url = 'https://www.douyin.com'
    try:
        driver.get(url)
    except Exception as e:
        logger.error("request first url fail: %s, err: %s" % (url, e))
        driver.quit()
        return False
    valid_code(driver)
    # count = 0
    # while True:
    #     if count >= 20:
    #         break
    #     time.sleep(4)
    #     try:
    #         driver.get_screenshot_as_file(source_img_path)
    #         area = get_target_image(driver)
    #         filter_template_image(area)
    #         get_template_image(driver)
    #         slide = get_slider(driver)
    #         distance = detect_target_location(target_img_path, template_img_path)
    #         # true_distance = distance + other_length
    #         tracks = get_track(distance)
    #         move2gap(driver, slide, tracks)
    #     except Exception as e:
    #         break
    #     time.sleep(2)
    #     count += 1
    driver.refresh()
    time.sleep(3)
    print("11111111111")
    print(driver.window_handles)
    driver.find_element_by_id("_285c63f4da53bd5cedc023b4fdd71412-scss").click()
    time.sleep(1)
    driver.find_element_by_class_name("web-login-normal-input__input").send_keys(13207123556)
    time.sleep(0.1)
    # driver.find_element_by_class_name("web-login-button-input__button-text send-input").click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/article/article/div[1]/div[1]/div[2]/article/div[2]/div/span').click()
    time.sleep(0.5)
    valid_code(driver)
    input_code = input("请输入手机验证码:")
    driver.find_element_by_class_name("web-login-button-input__input").send_keys(input_code)
    time.sleep(1)
    # driver.find_element_by_class_name("web-login-button web-login-button__disabled").click()
    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button').click()
    time.sleep(3)
    valid_code(driver)
    driver.find_element_by_class_name("_28bcf0c81eecec324dc834fd9da6bc14-scss").send_keys("好看的小姐姐")
    time.sleep(0.5)
    driver.find_element_by_class_name("btn-title").click()
    time.sleep(0.5)
    driver.refresh()
    time.sleep(5)
    all_handles = driver.window_handles
    print("222222222222")
    print(all_handles)
    # driver.switch_to_window(all_handles[-1])
    driver.switch_to.window(all_handles[-1])
    # ele = driver.find_element_by_class_name("_77aca3b4414e47c4bf4cd1b648feef96-scss")
    # ele = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[1]/div/div[1]/span[1]')
    # ActionChains(driver).move_to_element(ele)
    down_count = 0
    while True:
        time.sleep(random.choice((1, 1.3, 1.5, 1.7)))
        print(down_count)
        if down_count >= 5:
            break
        js_down = "var q=document.documentElement.scrollTop=%s" % random.choice((300, 500, 1000, 1200, 1500, 1800))
        # js_up = "var q=document.documentElement.scrollBottom=%s" % random.choice((110, 330, 550, 770, 990))
        driver.execute_script(js_down)
        down_count += 1
    time.sleep(10)
    driver.quit()


def valid_code(driver):
    count = 0
    while True:
        if count >= 20:
            print("赶紧通知来手动点一下")
            break
        time.sleep(3)
        try:
            driver.get_screenshot_as_file(source_img_path)
            area = get_target_image(driver)
            filter_template_image(area)
            get_template_image(driver)
            slide = get_slider(driver)
            distance = detect_target_location(target_img_path, template_img_path)
            tracks = get_track(distance)
            move2gap(driver, slide, tracks)
        except Exception as e:
            print("验证通过了,或者没有验证码")
            break
        count += 1


def get_template_image(driver):
    template_img = driver.find_element_by_id("captcha-verify-image")
    location = template_img.location
    size = template_img.size
    # print("template_image, location: %s, size: %s" % (location, size))
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
    # print(top, bottom, left, right)
    img = Image.open(filter_img_path)
    crop_img = img.crop((left, top, right, bottom))
    crop_img.save(template_img_path)


def get_target_image(driver):
    target_img = driver.find_element_by_xpath('//*[@id="captcha_container"]/div/div[2]/img[2]')
    location = target_img.location
    size = target_img.size
    # print("target_img, location: %s, size: %s" % (target_img.location, target_img.size))
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
    # print(top, bottom, left, right)
    img = Image.open(source_img_path)
    crop_img = img.crop((left, top, right, bottom))
    crop_img.save(target_img_path)
    return [left, top, right, bottom]


def filter_template_image(area):
    tem_img = Image.open(source_img_path)
    draw = ImageDraw.Draw(tem_img)
    draw.rectangle(area, fill=(255, 255, 255, 255))
    del draw
    tem_img.save(filter_img_path)


def get_slider(driver):
    slider = driver.find_element_by_xpath('//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
    # print("slider, location: %s, size: %s" % (slider.location, slider.size))
    return slider


def show_target(name):
    """
    展示检测的目标
    :param name:
    :return:
    """
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destoryAllWindows()


def filter_canny(image):
    """
    消除噪点
    :param image:
    :return:
    """
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


def detect_target_location(target_image, filter_template_image):
    image = cv2.imread(target_image, 0)
    template = cv2.imread(filter_template_image, 0)

    # 寻找最佳匹配
    res = cv2.matchTemplate(filter_canny(image), filter_canny(template), cv2.TM_CCOEFF_NORMED)
    # 最小值，最大值，并得到最小值, 最大值的索引
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc[0]  # 横坐标
    # 展示圈出来的区域
    # x, y = max_loc  # 获取x,y位置坐标
    #
    # w, h = image.shape[::-1]  # 宽高
    # cv2.rectangle(template, (x, y), (x + w, y + h), (7, 249, 151), 2)
    # show_target(template)
    print(top_left)
    return top_left


def get_track(distance):
    """
    :param distance: 移动距离
    :return: 运动轨迹
    先匀加速，后匀减速
    """
    tracks = []
    current = 0
    mid = distance * 4 / 5
    # 计算时间间隔
    t = 0.5
    # 初始速度
    v = 0
    while current < distance:
        if current < mid:
            a = 7
        else:
            a = -5
        # 初始速度
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        tracks.append(move)
    return tracks


def move2gap(driver, slider, tracks):
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


def test():
    pilim = Image.open("template.png")
    draw = ImageDraw.Draw(pilim)
    draw.rectangle([0, 0, 300, 300], fill=(255, 255, 255, 255))
    del draw
    pilim.save('2.png')


if __name__ == "__main__":
    # test()
    loading_page()
    # detect_target_location(target_img_path, template_img_path)
    # test()
