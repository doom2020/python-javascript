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


logger.add(r'C:\Users\yuanzhijian\Desktop\douyin.log')

video_path = r'E:\douyin\good_food'
if not os.path.exists(video_path):
    os.makedirs(video_path)

video_url_list = []
queue_video_url = queue.Queue(maxsize=10000)

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}


def loading_page():
    chrome_option = webdriver.ChromeOptions()
    # chrome_option.add_argument('--headless')
    # chrome_option.add_argument('--disable-gpu')
    # proxy = "--proxy-server=http://" + '175.7.199.129:3256'
    user_agent = "user-agent=" + headers['user-agent']
    # chrome_option.add_argument(proxy)
    chrome_option.add_argument(user_agent)
    driver = webdriver.Chrome(chrome_options=chrome_option)
    driver.set_page_load_timeout(random.randint(50, 80))
    url = 'https://www.douyin.com/channel/300204'
    try:
        driver.get(url)
    except Exception as e:
        logger.error("request first url fail: %s, err: %s" % (url, e))
        driver.quit()
        return False
    time.sleep(10)
    driver.refresh()
    while True:
        q_size = queue_video_url.qsize()
        if q_size >= 2000:
            break
        js_down = "var q=document.documentElement.scrollTop=%s" % random.choice((3300, 5500, 8800, 11000, 10050, 11010))
        js_up = "var q=document.documentElement.scrollBottom=%s" % random.choice((110, 330, 550, 770, 990))
        driver.execute_script(js_down)
        time.sleep(random.choice((0.1, 0.3, 0.5, 0.7)))
        driver.execute_script(js_up)
        time.sleep(random.choice((1.1, 2.2, 3.3)))
        page_html = driver.page_source
        parse_html(page_html)
        time.sleep(0.5)
    driver.quit()


def parse_html(page_html):
    pattern = re.compile('<li class="ff48959a07ac65915c5a5582a6d72fbe-scss">.*?<a href="(.*?)".*?</li>', re.S)
    result_ls = re.findall(pattern, page_html)
    if result_ls:
        for url in result_ls:
            if url not in video_url_list:
                video_url_list.append(url)
                queue_video_url.put(url)


def parse_detail():
    chrome_option = webdriver.ChromeOptions()
    user_agent = "user-agent=" + headers['user-agent']
    chrome_option.add_argument(user_agent)
    driver = webdriver.Chrome(chrome_options=chrome_option)
    driver.set_page_load_timeout(random.randint(50, 80))
    while True:
        url = queue_video_url.get(block=True, timeout=10*60)
        logger.info(url)
        if not url:
            driver.quit()
            break
        try:
            driver.get(url)
        except Exception as e:
            logger.error("request second url fail: %s, err: %s" % (url, e))
            continue
        time.sleep(5)
        driver.refresh()
        time.sleep(2)
        page_html = driver.page_source
        pattern = re.compile('</canvas>.*?src="(.*?)">', re.S)
        result_ls = re.findall(pattern, page_html)
        if result_ls:
            url = "https:" + result_ls[0]
            logger.info(url)
            retry_count = 0
            while True:
                if retry_count >= 3:
                    logger.error("request detail url fail: %s" % url)
                    break
                resp = requests.get(url, headers=headers, stream=True)
                logger.info(resp.status_code)
                if resp.status_code != 200:
                    retry_count += 1
                    continue
                md5 = hashlib.md5()
                md5.update(url.encode('utf-8'))
                file_name = md5.hexdigest()
                file_path = os.path.join(video_path, file_name) + '.mp4'
                logger.info(file_path)
                with open(file_path, 'wb') as fw:
                    for chuck in resp.iter_content(chunk_size=4096):
                        fw.write(chuck)
                break
        else:
            logger.error("request second url invalid: %s" % url)


def dealwith_task():
    tp = ThreadPoolExecutor(max_workers=4)
    tp.submit(parse_detail)
    tp.shutdown(wait=True)


if __name__ == "__main__":
    begin_time = str(datetime.now())
    t1 = threading.Thread(target=loading_page)
    t1.start()
    time.sleep(10)
    t2 = threading.Thread(target=dealwith_task)
    t2.start()
    t1.join()
    t2.join()
    end_time = str(datetime.now())
    print("开始时间: %s, 结束时间: %s" % (begin_time, end_time))
