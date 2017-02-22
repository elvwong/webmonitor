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
def getData():
    sql = ""
    #提交方式为POST：
    if request.method == "POST":
        #1、接收客户端提交的JSON数据
        data = request.json
        try:
            #2、拆分数据、拼装SQL语句
            #sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) 
            #VALUES('%s', '%d', '%d', '%d', '%s', '%d')" % (data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], int(data['Time']))
            sql = "INSERT INTO `stat` (`host`,`mem_free`,`mem_usage`,`mem_total`,`time`) \
                VALUES('%s', '%d', '%d', '%d', '%d')" % (data['host'], int(data['mem_free']), int(data['mem_used']), int(data['mem_total']), int(data['time']))
            #3、执行SQL，将数据入库
            ret = c.execute(sql)
        except mysql.IntegrityError:
            pass
        #finally:  
            #pass  
        return "OK"
    #提交方式为GET：
    else:
        return render_template("index.html")
    
#根据传入的host参数查询不同计算机的内存数据
@app.route("/data/<host>", methods=["GET"])
def getdata(host):
    print 'host:',host
    #1、根据传入的host参数拼装SQL
    sql = "SELECT `time`,`mem_usage` FROM `stat` where `host`='%s'" %host
    #2、执行SQL，查询不同计算机的内存数据
    c.execute(sql)
    #3、拆分返回的数据，拼装列表
    ones = [[i[0]*1000, i[1]] for i in c.fetchall()]
    #4、将列表转换为JSON返回给客户端
    return "%s(%s);" % (request.args.get('callback'), json.dumps(ones))
    

if __name__ == "__main__":
    #启动服务器，设置端口：8888
    app.run(host="0.0.0.0", port=8888, debug=True)
