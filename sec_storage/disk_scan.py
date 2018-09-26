#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: disk_scan.py
__author__ = 'wz'


import os

SCAN_SIZE=52428800


def reduce_lines(contents):
    ret = ""
    a = contents.splitlines(True)
    for i,item in enumerate(a):
        if i >=11:
            break
        ret += item
    return ret

def get_vm_disk_size(vm_disk_path):
#     global IS_ERROR
#     if IS_ERROR==True or vm_disk_path=="":
#         return "0"
    try:
        file_info=os.popen('ls -l %s'%(vm_disk_path)).read().split(' ')
        return file_info[4]
    except:
        return "0"

def do_scan(disk_path,disk_size,symbol):
    scan_count=disk_size/SCAN_SIZE
    is_contain = False
    for i in range(0,scan_count):
        scan_content=os.popen('hexdump -C %s -n %s -s %s | grep "[_ .:]%s[_ .:]" -C 1 | more' \
                  %(disk_path,SCAN_SIZE,SCAN_SIZE*i,symbol)).read()
        if(len(scan_content)!=0):
            scan_content = reduce_lines(scan_content)
            result = "matching succeed" + "<br>" + scan_content +"<br>"
            is_contain = True
            break
    if not is_contain:
        result = "matching failed"
#     if(is_contain==True and need_print==True):
#         result = result + "<br>" + scan_content +"<br>"
    return result

def symbol_scan(disk_path, disk_size):
    detail = "<font size='5'>start disk scanning:</font>"
    detail += "<br>vm_disk_size:" + str(disk_size)
#     windows_symbol_list=['microsoft','windows']
#     linux_symbol_list=['linux','jiffies']
    symbol_list=['boot', 'root', 'environment', 'path', 'service', 'user', 'password']
    if disk_size==0:
        return "ERROR!无法获取磁盘空间信息"
    try:
        is_contain=True
        for symbol in symbol_list:
            scan_result = do_scan(disk_path,disk_size,symbol)
            detail += "<br>keyword:"+symbol + "<br>" + scan_result
            if scan_result == "matching failed":
                is_contain=False
                break
        detail += "<br>scanning over"
        if is_contain:
            result = "VM disk is NOT encrypted"
        else:
            result = "VM disk MAY BE encrypted"
        ret = {"result" : result, "detail" : detail}
        return ret
    except:
        return "ERROR,扫描出现未指定错误"

if __name__ == "__main__":
    vm_disk_path = "/kvm/images/c8f5ff0c-52b5-490b-b9b4-d11b5e0e78e2/images/1aebe17c-f885-4f58-9a60-5307d700d88a/ec64733d-a88e-4325-8298-a09102946823"
    
    vm_disk_size=int(get_vm_disk_size(vm_disk_path))
    print symbol_scan(vm_disk_path,vm_disk_size)