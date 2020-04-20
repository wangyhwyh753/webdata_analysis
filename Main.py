#!/usr/bin/env python
import pymysql
#from pyhive import hive
from flask import Flask
from flask import render_template
from flask import request,redirect,url_for,send_file
#from datetime import datetime
#from data_to_influxdb import HqlDataToInfluxdbManager
#from hive_operator import HiveManager
#from influxdb import InfluxDBClient
from ldaptest import check_valid
import json
import pandas as pd
from flask_cors import CORS
# import numpy as np
import math

app = Flask(__name__)
CORS(app,supports_credentials=True,resources=r'/*')
def check_mysql(sql,type):
    if type == 1:
        try:
            Conn_m = pymysql.Connect('localhost', 'root', 'Wangyhwyh@753','news',charset='utf8')
            cursor = Conn_m.cursor()
            cursor.execute(sql)

            #result = cursor.fetchall()
            #return result
            columns = [col[0] for col in cursor.description]
            # # print(columns)
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            hql_frame = pd.DataFrame(result, columns=columns)
            data_temp = []
            index = 1
            for row in hql_frame.itertuples():
                temp_dict = {}
                for item in columns:
                    if item == 'time_d':
                        temp_dict[item] = getattr(row,item).strftime("%Y-%m-%d")
                    elif item == 'time_m':
                        temp_dict[item] = getattr(row, item).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        temp_result = getattr(row, item)
                        if isinstance(temp_result,(int,float)):
                            if math.isnan(temp_result):
                                temp_dict[item] = None
                            else:
                                temp_dict[item] = temp_result
                        else:
                            temp_dict[item] = temp_result
                temp_dict['sort'] = index
                index += 1
                data_temp.append(temp_dict)
            cursor.close()
            Conn_m.close()
            return data_temp
        except Exception as e:
            print(e)
            return False
    elif type == 2:
        try:
            Conn_m = pymysql.Connect('cpu35.aibee.cn', 'root', 'warehouse','data_tagging',charset='utf8')
            cursor = Conn_m.cursor()
            cursor.execute(sql)
            #columns = [col[0] for col in cursor.description]
            # # print(columns)
            result = cursor.fetchall()
            # name_list = hql_frame.columns.tolist()
            # name_list_new = []
            # for name_list_item in name_list:
            #     num_index = name_list_item.find('.')
            #     name_new = name_list_item[(num_index + 1):]
            #     name_list_new.append(name_new)
            # hql_frame.columns = name_list_new
            # print(hql_frame)
            # data_temp = []
            # for row in hql_frame.itertuples():
            #     temp_dict = {}
            #     for item in columns:
            #         if item == 'date':
            #             temp_dict[item] = getattr(row,item).strftime("%Y-%m-%d")
            #         else:
            #             temp_dict[item] = getattr(row, item)
            #     data_temp.append(temp_dict)
            cursor.close()
            Conn_m.close()
            return result
        except Exception as e:
            print(e)
            return False
    else:
        try:
            Conn_m = pymysql.Connect('cpu35.aibee.cn', 'root', 'warehouse', 'data_tagging',charset='utf8')
            cursor = Conn_m.cursor()
            cursor.execute(sql)
            Conn_m.commit()
            cursor.close()
            Conn_m.close()
            return True
        except Exception as e:
            print(e)
            return False
@app.route('/')
def main_html():
    print('已经进入网站')
    return render_template("login.html")

@app.route('/deal_login', methods=['GET','POST'])
def deal_login():
    data_dict_json = request.args.get('data','')
    data_dict = json.loads(data_dict_json)
    print(data_dict)
    user_name = data_dict['user_name']
    pass_word = data_dict['pass_word']
    result = check_valid(user_name,pass_word)

    if result:
        return "ok"
    else:
        return "false"

@app.route('/deal_baidu_current_hot', methods=['GET','POST'])
def deal_baidu_current_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE `time_m` >= DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 120 MINUTE),'%Y-%m-%d %H') and `source`="baidu"  ORDER BY `nums` DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)

@app.route('/deal_baidu_month_hot', methods=['GET','POST'])
def deal_baidu_month_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE date(`time_d`) >= TO_DAYS(DATE_SUB(CURDATE(),INTERVAL 30 DAY)) and `source`="baidu"  ORDER BY nums DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)

@app.route('/deal_baidu_week_hot', methods=['GET','POST'])
def deal_baidu_week_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE date(`time_d`) >= TO_DAYS(DATE_SUB(CURDATE(),INTERVAL 7 DAY)) and `source`="baidu"  ORDER BY nums DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)

@app.route('/deal_baidu_year_hot', methods=['GET','POST'])
def deal_baidu_year_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE date(`time_d`) >= TO_DAYS(DATE_SUB(CURDATE(),INTERVAL 90 DAY)) and `source`="baidu"  ORDER BY nums DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)


@app.route('/deal_weibo_current_hot', methods=['GET','POST'])
def deal_weibo_current_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE `time_m` >= DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 120 MINUTE),'%Y-%m-%d %H') and `source`="weibo"  ORDER BY `nums` DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)

@app.route('/deal_weibo_month_hot', methods=['GET','POST'])
def deal_weibo_month_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE date(`time_d`) >= TO_DAYS(DATE_SUB(CURDATE(),INTERVAL 1 month)) and `source`="weibo"  ORDER BY nums DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)

@app.route('/deal_weibo_week_hot', methods=['GET','POST'])
def deal_weibo_week_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE date(`time_d`) >= TO_DAYS(DATE_SUB(CURDATE(),INTERVAL 7 DAY)) and `source`="weibo"  ORDER BY nums DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)

@app.route('/deal_weibo_year_hot', methods=['GET','POST'])
def deal_weibo_year_hot():
    page = int(request.args.get('page', ''))
    limit = int(request.args.get('limit', ''))
    sql = """select * from news_statistic WHERE date(`time_d`) >= TO_DAYS(DATE_SUB(CURDATE(),INTERVAL 3 month)) and `source`="weibo"  ORDER BY nums DESC LIMIT 10"""
    data_list = check_mysql(sql, 1)
    print(data_list)
    length = len(data_list)
    data = {"code": 0, "msg": "", "count": length, "data": data_list[((page - 1) * limit):(page * limit)]}
    return json.dumps(data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9526)