import requests
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import pandas as pd
import pymysql

#获取当前日期
def get_date():
    return (datetime.today()+timedelta(days=0)).strftime("%Y-%m-%d")
# 程序开始执行
def begin_task():
    print("task begin %s"%(datetime.today().strftime("%Y-%m-%d")))
    # 任务列表
    task_name = 'get_hot_link'
    # task_name_beijing_tzwd =  'ods.wanda-beijing-tzwd.pid_mapping'
    # # 报警标题
    # title1 = "ods.k11-guangzhou-mall.pid_mapping在%s日任务没有完成，请检查"%(get_date())
    # title2 = "ods.wanda-beijing-tzwd.pid_mapping在%s日任务没有完成，请检查"%(get_date())
    # #检查异常报警
    check_task(task_name)
    #     alert(title1,title1,'15518578973','wcma@aibee.cn')
    # if check_task(task_name_beijing_tzwd):
    #     alert(title2,title2,'15518578973','wcma@aibee.cn')
    print("task end %s"%(datetime.today().strftime("%Y-%m-%d")))

# 加载chrome的驱动
def check_task(task_name):
    # 获取模拟浏览器
    print("driver init Begin()")
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # #chrome_options.add_argument(r"user-data-dir=/usr/local")
    # #chrome_options.add_argument("window-size=1024,768")
    # # 添加沙盒模式
    # chrome_options.add_argument("--no-sandbox")
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    # #browser = webdriver.Chrome()

    # 登录后才能访问的网页
    # url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E7%83%AD%E6%90%9C&rsv_pq=e583a97400014041&rsv_t=8e12yatMTX%2Fvz8tgtp%2B87sKZo1JvrdLzraWmjwhtc0R6r%2Fgfm9xugj03jAM&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=17&rsv_sug1=26&rsv_sug7=101&rsv_sug2=0&inputT=6207&rsv_sug4=7323"
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=table&oq=%25E7%2583%25AD%25E6%2590%259C&rsv_pq=bc4788a800009bdf&rsv_t=5bf3Zg6sFIcKYYqPqffagTRc%2BPdrZhN8bmpT%2BpVCGR3CpJvOPYEfdZ%2BW8yY&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=6207&rsv_sug3=26&rsv_sug1=33&rsv_sug7=101&bs=%E7%83%AD%E6%90%9C"
    parser_html(url,"baidu")
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    parser_html(url,"weibo")


#通过用户名和密码，没有通过cookies的方式登陆
def parser_html(url,data_source):
    # driver.delete_all_cookies()
    # '''通过request 登陆系统，获取cookie'''
    # driver.get(url)
    # print(driver.current_url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    # 例子的url
    # url = 'https://voice.hupu.com/nba'  # 虎扑nba新闻
    # 利用requests对象的get方法，对指定的url发起请求
    # 该方法会返回一个Response对象
    res = requests.get(url, headers=headers)
    # 通过Response对象的text方法获取网页的文本信息
    # print(res.text)
    try:
        conn = pymysql.connect('127.0.0.1', user='root', password='Wangyhwyh@753', database='news')
    except Exception as e:
        print(e)
    cursor = conn.cursor()

    time_day = datetime.today().strftime("%Y-%m-%d")
    time_min = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    if data_source == "baidu":
        print("baidu begin")
        # 下面的方法找出了所有class为hello的span标签
        # 并将所有的结果都放入一个list返回
        soup = BeautifulSoup(res.text, 'lxml')
        tags = soup.find('table', {'class': 'c-table opr-toplist1-table'})
        tr_list = tags.find_all('tr')
        index = 1

        # year_temp,month_temp,day_temp = date_temp.split('-')
        # hours_temp = datetime.now().strftime("%H:%M:%S")
        # time_temp = date_temp + ' ' + hours_temp
        news_type = 0
        for tr in tr_list:
            try:
                title = tr.find('a').get_text().strip()
                url_temp = "https://www.baidu.com"+tr.find('a')['href'].strip()
                news_temp = tr.find('td',{'class':'opr-toplist1-right'}).get_text().strip()
                index_l = news_temp.find('万')
                if index_l > 0:
                    num_temp = int(news_temp[:index_l])*10000
                else:
                    num_temp = int(news_temp)
                cmd = "select `nums` from news_statistic where `title` = '%s' "%(title)
                cursor.execute(cmd)
                result = cursor.fetchall()
                if result:
                    num_temp_exist = result[0][0]
                    if num_temp_exist > num_temp:
                        pass
                    else:
                        cmd = "insert into news_statistic(`time_d`,`time_m`,`title`,`url`,`nums`,`source`,`current_sort`,`news_type`) values " \
                              "('%s','%s','%s','%s',%d,'%s',%d,%d)" \
                              "ON DUPLICATE KEY UPDATE `time_d`='%s',`time_m` = '%s',`url`='%s',`nums`=%d,`source`='%s',`current_sort`=%d,`news_type`=%d" % (
                                  time_day,time_min, title, url_temp, num_temp,
                                  data_source, index, news_type, time_day,time_min, url_temp, num_temp, data_source, index,
                                  news_type)
                        cursor.execute(cmd)
                        conn.commit()
                        index += 1
                else:
                    cmd = "insert into news_statistic(`time_d`,`time_m`,`title`,`url`,`nums`,`source`,`current_sort`,`news_type`) values " \
                          "('%s','%s','%s','%s',%d,'%s',%d,%d)" \
                          "ON DUPLICATE KEY UPDATE `time_d`='%s',`time_m` = '%s',`url`='%s',`nums`=%d,`source`='%s',`current_sort`=%d,`news_type`=%d" % (
                              time_day, time_min, title, url_temp, num_temp,
                              data_source, index, news_type, time_day, time_min, url_temp, num_temp, data_source, index,
                              news_type)
                    cursor.execute(cmd)
                    conn.commit()
                    index += 1
            except Exception as e:
                conn.rollback()
                print(e)
    elif data_source == "weibo":
        print("weibo begin")
        # 下面的方法找出了所有class为hello的span标签
        # 并将所有的结果都放入一个list返回
        soup = BeautifulSoup(res.text, 'lxml')
        firstpart = soup.find('div', {'id': 'pl_top_realtimehot'})
        table_part = firstpart.find('tbody')
        tr_list = table_part.find_all('tr')
        index = 1
        # year_temp, month_temp, day_temp = date_temp.split('-')
        # hours_temp = datetime.now().strftime("%H:%M:%S")
        # time_temp = date_temp + ' ' + hours_temp
        news_type = 0
        for tr in tr_list:
            try:
                title = tr.find('a').get_text().strip()
                url_temp = "https://s.weibo.com" + tr.find('a')['href'].strip()
                news_temp = tr.find('span').get_text().strip()
                index_l = news_temp.find('万')
                if index_l > 0:
                    num_temp = int(news_temp[:index_l]) * 10000
                else:
                    num_temp = int(news_temp)
                cmd = "select `nums` from news_statistic where `title` = '%s' " % (title)
                cursor.execute(cmd)
                result = cursor.fetchall()
                if result:
                    num_temp_exist = result[0][0]
                    if num_temp_exist > num_temp:
                        pass
                    else:
                        cmd = "insert into news_statistic(`time_d`,`time_m`,`title`,`url`,`nums`,`source`,`current_sort`,`news_type`) values " \
                              "('%s','%s','%s','%s',%d,'%s',%d,%d)" \
                              "ON DUPLICATE KEY UPDATE `time_d`='%s',`time_m` = '%s',`url`='%s',`nums`=%d,`source`='%s',`current_sort`=%d,`news_type`=%d" % (
                                  time_day, time_min, title, url_temp, num_temp,
                                  data_source, index, news_type, time_day, time_min, url_temp, num_temp, data_source, index,
                                  news_type)
                        cursor.execute(cmd)
                        conn.commit()
                        index += 1
                else:
                    cmd = "insert into news_statistic(`time_d`,`time_m`,`title`,`url`,`nums`,`source`,`current_sort`,`news_type`) values " \
                          "('%s','%s','%s','%s',%d,'%s',%d,%d)" \
                          "ON DUPLICATE KEY UPDATE `time_d`='%s',`time_m` = '%s',`url`='%s',`nums`=%d,`source`='%s',`current_sort`=%d,`news_type`=%d" % (
                              time_day, time_min, title, url_temp, num_temp,
                              data_source, index, news_type, time_day, time_min, url_temp, num_temp, data_source, index,
                              news_type)
                    cursor.execute(cmd)
                    conn.commit()
                    index += 1
            except Exception as e:
                conn.rollback()
                print(e)


if __name__ == "__main__":
    begin_task()
    pass
