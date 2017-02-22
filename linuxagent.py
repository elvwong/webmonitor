#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2017年2月13日

@author: wangyong
'''

import time   
import urllib, urllib2
import json

class LinuxAgent():
    '''
    linux 采集数据
    '''
 
    def __init__(self, params):
        pass
    #系统内存信息：/proc/meminfo 文件包含系统内存的详细信息，其中显示物理内存的数量、可用交换空间的数量，以及空闲内存的数量等。
    def get_mem_info(self):
        with open('/proc/meminfo') as f:
            total = int(f.readline().split()[1])
            free = int(f.readline().split()[1])
            buffers = int(f.readline().split()[1])
            cache = int(f.readline().split()[1])
        mem_use = total - free - buffers - cache
        data = {}
        data['host'] = '192.168.245.132'
        data['mem_total'] = total
        data['mem_used'] = mem_use
        data['mem_free'] = free
        data['time'] = time.time()
        print mem_use / 1024
        return data

if __name__ == '__main__':        
    while True:
        
        la = LinuxAgent()
        data = la.get_mem_info()  
        
        print u"内存使用率: " ,data,json.dumps(data)
        req = urllib2.Request("http://192.168.245.36:8888/", json.dumps(data), {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        print response
        f.close()
        time.sleep(5)
