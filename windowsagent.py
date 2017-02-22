# coding=utf8

'''
Created on 2017年2月9日

@author: wangyong
'''
import psutil
import time   
import urllib, urllib2
import json 

class Winsysinfo:    
    
    cpu = {'user' : 0, 'system' : 0, 'idle' : 0, 'percent' : 0}
    mem = {'total' : 0, 'avaiable' : 0, 'percent' : 0, 'used' : 0, 'free' : 0}     
    # 磁盘名称
    disk_id = []
    # 将每个磁盘的total used free percent 分别存入到相应的list
    disk_total = []
    disk_used = []
    disk_free = []
    disk_percent = []    
   
    def __init__(self):
        pass
    # 获取CPU信息
    def get_cpu_info(self):
        cpu_times = psutil.cpu_times()
        self.cpu['user'] = cpu_times.user
        self.cpu['system'] = cpu_times.system
        self.cpu['idle'] = cpu_times.idle
        self.cpu['percent'] = psutil.cpu_percent(interval=2)
    # 获取内存信息
    def get_mem_info(self):
        mem_info = psutil.virtual_memory()
        self.mem['total'] = mem_info.total/1024/1024
        self.mem['available'] = mem_info.available/1024/1024
        self.mem['percent'] = mem_info.percent
        self.mem['used'] = mem_info.used/1024/1024
        self.mem['free'] = mem_info.free/1024/1024
    # 获取磁盘
    def get_disk_info(self):
        for id in psutil.disk_partitions():
            if 'cdrom' in id.opts or id.fstype == '':
                continue
            disk_name = id.device.split(':')
            s = disk_name[0]
            self.disk_id.append(s)
            disk_info = psutil.disk_usage(id.device)
            self.disk_total.append(disk_info.total)
            self.disk_used.append(disk_info.used)
            self.disk_free.append(disk_info.free)
            self.disk_percent.append(disk_info.percent)
             
            
    
    
if __name__ == '__main__':
    
    while True:        
        test = Winsysinfo()
        test.get_cpu_info()
        cpu_status = test.cpu['percent']
        print u"CPU使用率: %s %%" % cpu_status
        #1、获取系统内存信息
        test.get_mem_info()
        mem_status = test.mem['percent']
        mem_total = test.mem['total']
        mem_available = test.mem['available']
        mem_used = test.mem['used']
        mem_free = test.mem['free']
        #2、封装需要上传的数据
        data = {}
        data['host'] = 'localhost'    #监控的计算机IP
        data['mem_total'] = mem_total #内存总计
        data['mem_used'] = mem_used   #已使用
        data['mem_free'] = mem_free   #空闲
        data['time'] = time.time()
        print u"内存使用率: %s %%" % mem_status,mem_total,mem_used,mem_free,json.dumps(data)
        #3、将封装数据转换为JSON格式后提交至指定web服务：http://localhost:8888/，由服务器处理数据
        #   urllib2是python的一个获取url（Uniform ResourceLocators，统一资源定址器）的模块。
        req = urllib2.Request("http://localhost:8888/", json.dumps(data), {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        print response
        f.close()
        #4、休眠3秒后继续执行
        time.sleep(3)    
       
