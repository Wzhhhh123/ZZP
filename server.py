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
# @app.route('/pa.html')
# def pa():
#     return render_template('form-advanced.html')
#
# @app.route('/papa',methods=["GET", "POST"])
# def papa1():
#     lei = request.args.get('lei')
#
#     ccc=papa(lei)
#     return ccc




if __name__ == "__main__":
    app.run(debug = True,host='0.0.0.0',port=802)

