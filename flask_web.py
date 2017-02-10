#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2017年2月8日

@author: wangyong
'''
import MySQLdb as mysql
import json
from flask import Flask, request, render_template
app = Flask(__name__)
db = mysql.connect(user="root", passwd="sa", \
        db="wy", charset="utf8")
db.autocommit(True)
c = db.cursor()

@app.route("/", methods=["GET", "POST"])
def hello():
    sql = ""
    if request.method == "POST":
        data = request.json
        try:
            #sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s', '%d')" % (data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], int(data['Time']))
            sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES(`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`)" 
            ret = c.execute(sql)
        except mysql.IntegrityError:
            pass
        #finally:  
            #pass  
        return "OK"
    else:
        return render_template("index.html")

@app.route("/data", methods=["GET"])
def getdata():
    c.execute("SELECT `time`,`mem_usage` FROM `stat`")
    ones = [[i[0]*1000, i[1]] for i in c.fetchall()]
    return "%s(%s);" % (request.args.get('callback'), json.dumps(ones))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
