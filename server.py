import json
from random import randrange
from flask.json import jsonify
from flask import Flask, render_template,url_for,request,session,flash,redirect
import pandas as pd
import requests
import re
import os
import csv
from pyecharts import options as opts
from pyecharts.charts import Line,Bar
import time
import datetime
from flask_cors import CORS,cross_origin
from functools import wraps
from mysql_util import MysqlUtil
from Code.wei import time_formater,get_single_page,getLongText,parse_page,kaishi
from Code.upload import main
from Code.commentspy import pinglun
def date_delta(date,gap,formate = "%Y%m%d"):
        date = str2date(date)
        pre_date = date + datetime.timedelta(days=-gap)
        pre_str = date2str(pre_date,formate)  # date形式转化为str
        return pre_str
def str2date(str,date_format="%Y%m%d"):
    date = datetime.datetime.strptime(str, date_format)
    return date
def date2str(date,date_formate = "%Y%m%d"):
    str = date.strftime(date_formate)
    return str
app = Flask(__name__, static_folder="templates")

@app.route('/index.html')
def index():

    return render_template('index.html')
# @app.route('/table')
# def table():
#     ta  = request.args.get('ta')
#
#     if (ta=="user"):
#         sql=f'SELECT * FROM `wangyi`'
#         db = MysqlUtil()
#         dd = db.fetchall(sql)
#         return render_template('table_user.html')
#     sql=f'SELECT * FROM `wangyi`'
#     db = MysqlUtil()
#     dd = db.fetchall(sql)
#     return render_template('table.html',dd=dd)
# @app.route('/dashboard-crm.html')
# def Dashboard():
#     return render_template('dashboard-crm.html')
# @app.route('/maps-vector.html')
# def map():
#     return render_template('maps-vector.html')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    form-advanced.html
@app.route('/paaotu.html')
def pa():
    db = MysqlUtil()  # 实例化数据库操作类
    page = request.args.get('page')  # 获取当前页码
    if page is None:  # 默认设置页码为1
        page = 0
    # 分页查询
    # 从article表中筛选5条数据，并根据日期降序排序
    m=re.findall("\d+", str(time.strftime("%Y-%m-%d", time.localtime())))
    m=m[0]+m[1]+m[2]
    m=date_delta(m,int(page))
    kk=m[0:4]+"-"+m[4:6]+"-"+m[6:8]
    sql = f'SELECT * FROM weibohot where create_date="{kk}"'
    articles = db.fetchall(sql)  # 获取多条记录
    return render_template('table-data.html',articles=articles, page=int(page))


@app.route('/hot')
def hot1():
    title = request.args.get('title')
    sql= f'SELECT * FROM weiboevent where title="{title}"'
    db = MysqlUtil()
    articles = db.fetchall(sql)

    return render_template('hot.html',articles=articles, title=title)
@app.route('/lockscreen.html')
def lockscreen():
    return render_template('lockscreen.html')
#
@app.route('/upload',methods=["GET", "POST"])
def papa1():
    main()
    return jsonify("更新成功")

@app.route('/add',methods=["GET", "POST"])
def addevent():

    import os,csv
    global count
    count=0
    save_per_n_page = 5
    event = request.args.get('title')

    keyword=event
    result_file = f'{keyword}.csv'

    if not os.path.exists(result_file):
        with open(result_file, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['wid', 'user_name', 'user_id', 'gender',
                             'publish_time', 'text', 'like_count', 'comment_count',
                             'forward_count','status_city','status_country','status_province'])
    temp_data = []
    empty_times = 0

    for page in range(0, 5):  # 瀑布流下拉式，加载
        print(f'page: {page}')
        json_data = get_single_page(page, keyword)
        if json_data == None:
            print('json is none')
            break

        if len(json_data.get('data').get('cards')) <= 0:
            empty_times += 1
        else:
            empty_times = 0
        if empty_times > 3:
            print('\n\n consist empty over 3 times \n\n')
            break
        for result in parse_page(json_data):  # 需要存入的字段

            count=result['counts']
            temp_data.append(result)
        if page % save_per_n_page == 0:
            with open(result_file, mode='a+', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                for d in temp_data:
                    writer.writerow(
                        [d['wid'], d['user_name'], d['user_id'], d['gender'],
                         d['publish_time'], d['text'], d['like_count'], d['comment_count'],
                         d['forward_count'],d['status_city'],d['status_country'],d['status_province']])
            print(f'\n\n------cur turn write {len(temp_data)} rows to csv------\n\n')

    import csv
    import emoji
    title=event
    with open(title+'.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_csv = list(csv_reader)

    for kk in range(len(list_of_csv)-1):
        kk = kk + 1
        ss=list_of_csv[kk][5]
        import demoji
        res = emoji.replace_emoji(ss, replace=" ")
        if res!=ss:
            for o in demoji.findall(ss).values():
                res=res+''
                res=res+o
            list_of_csv[kk][5]=res
        sql = "INSERT INTO weiboevent(status_city,status_country,status_province,wid,title,user_id,user_name,gender,publish_time,text,like_count,comment_count,forward_count) \
                           VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%d','%d','%d')" % (list_of_csv[kk][-1], list_of_csv[kk][-2], list_of_csv[kk][-3], list_of_csv[kk][0], title,list_of_csv[kk][2],list_of_csv[kk][1],list_of_csv[kk][3],list_of_csv[kk][4],list_of_csv[kk][5],int(list_of_csv[kk][6]),int(list_of_csv[kk][7]),int(list_of_csv[kk][8]))
        db = MysqlUtil()
        db.insert(sql)

    return temp_data

@app.route('/pinglun',methods=["GET", "POST"])
def ping():
    url =  request.args.get('url')
    pinglun(url)
    return jsonify("评论成功")
@app.route('/comm')
def pingl():
    url =  request.args.get('url')
    title =  request.args.get('title')
    return render_template('charts.html',url=url,title=title)
@app.route('/pingluntu',methods=["GET", "POST"])
def pingluntu():
    import base64
    encoded = base64.b64encode(open('5.png', 'rb').read()).decode('ascii')
    return encoded

if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port=802)


