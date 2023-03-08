from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
import time,re
import json
from selenium.webdriver.common.by import By
def pinglun():
    option = FirefoxOptions()
    option.add_argument("--headless")  # 隐藏浏览器
    driver=Firefox(executable_path='geckodriver')
    driver.delete_all_cookies()
    driver.get('https://weibo.com/2803301701/Mwhn6FzxV')
    with open('Code/cookies.txt','r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        for cookie in cookies_list:
            driver.add_cookie(cookie)
    # 记得写完整的url 包括http和https
    time.sleep(2)
    driver.get('https://weibo.com/2803301701/Mwhn6FzxV')
    time.sleep(5)
    input=driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/textarea")
    input.send_keys('节日快乐')
    driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/button").click()
    commet=driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/div[2]/div[3]/div/div/div/div/div/div/div[1]/div/div/div/div/div[1]")
    commet.screenshot('5.png')
    return commet.screenshot('5.png')