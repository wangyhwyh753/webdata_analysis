import requests
import sys
import io
from selenium import webdriver
import time


def load_html():
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码
    browser = webdriver.Chrome()
    #建立Phantomjs浏览器对象，括号里是phantomjs.exe在你的电脑上的路径
    #browser = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-macosx/phantomjs-2.1.1-macosx/bin/phantomjs')
    #登录页面
    url = 'http://cpu32.aibee.cn:4081/static/node.html'
    # 访问登录页面
    browser.get(url)
    # 等待一定时间，让js脚本加载完毕
    time.sleep(2)
    res = browser.page_source
    print(res)
    #输入用户名
    username = browser.find_element_by_name('username')
    time.sleep(10)
    username.send_keys('yhwang')
    #输入密码
    password = browser.find_element_by_name('password')
    password.send_keys('Wangyhwyh@753')
    #选择“学生”单选按钮
    #student = browser.find_element_by_xpath('//input[@value="student"]')
    #student.click()
    #点击“登录”按钮
    login_button = browser.find_element_by_xpath('//form[@class="login"]')
    login_button.submit()
    # 等待一定时间，让js脚本加载完毕
    browser.implicitly_wait(3)
    res2 = browser.page_source
    print(res2)
    #网页截图
    #browser.save_screenshot('picture1.png')
    #打印网页源代码
    #print(browser.page_source.encode('utf-8').decode()）

    browser.quit()


if __name__ == "__main__":
    load_html()
