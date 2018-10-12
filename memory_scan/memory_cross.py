# coding=utf-8
'''
Created on Apr 22, 2016

@author: root
'''
# from sos.plugins import sysvipc
# import MySQLdb
'''
孙浩实现
'''

################################################################################################
def getallvm_mem():
    import os, sys, time
    child = os.popen("virsh list")
    r = child.read()
    output = open("/getall.txt", "w")
    output.writelines(r)
    output.close()
    list = {}
    file1 = open("/getall.txt", "r")
    lines = file1.readlines() 
    i = 2
    while(i < len(lines) - 1):
        lin = lines[i]
        s_id = lin[1:6]
        s_name = lin[7:]
        list.setdefault(s_id, s_name)
        i = i + 1
    file2 = open("/getall.txt", "w")
    file2.truncate()
    file2.close()
    report = "虚拟机列表信息如下:<br>"
    for id in list:
        theid = int(id)
        childs = os.popen("virsh dommemstat %s" % theid)
        report += "虚拟机名称:  "
        report += list[id]
        report += " 内存信息:"
        report += childs.read()
        report += "<br>"
    print report               
    return report
################################################################################################
# neicun bu fen 


def memory_scan():
    import os
    import sys
    reload(sys)
    print 'start memory_scan'
    strs = os.popen("pidof 'qemu-kvm'").read()
    strq = strs.strip('\n ').split(' ')
    if len(strq) < 2 :
        thereport = "主机中不存在虚拟机或者虚拟机的数量小于2台"
        historydir = os.getcwd()
        print historydir
        return thereport
        # 这里将thereport写入数据库
    else:
        # 切换工作目录
        current_path = os.getcwd()
        print current_path
        os.chdir(current_path + "/memory_scan/umuery")
        os.system("rm -rf v_result")
        memory_scan_details()
        # 获取当前工作目录路径
        currenrdir = os.getcwd()
        print currenrdir
        print "当前工作目录"
        if (os.path.getsize(currenrdir) == 0):
        # 判断
            ret = "未找到交叉的内存单元:"
        else:
            ret = "找到交叉的内存单元:"
            ret += "详细内容查看测试节点:"
            ret += "\n"
            ret += "路径:"
            ret += "\n"
            ret += os.getcwd() + "/v_result"
    
        print "22222"
        # 拼接测试报告的值：
        thereport = "%s \n" % ret 
        
        # 在这里进行文件大小的判断，如果大于1024k就返回文件地址，否则就直接让用户进行查看
        os.chdir("../../../")
    print "have the report?"
    print  thereport
    historydir = os.getcwd()
    print historydir
    print historydir
    print 'the report:', thereport

    return thereport


def memory_scan_details():
    print "this is memory_scan_details"
    import os
    current_path = os.getcwd()
    path = [current_path]
    str = os.popen("pidof 'qemu-kvm'").read()
    a = str.split("\n")
    cc = a[0]
    strq = cc.split(" ") # strq代表的是所有虚拟机进程的节点
    v_id1 = int(strq[0])
    del strq[0]
    slens = len(strq)
    i = 1
    for sl in strq:
        v_id2 = int(sl)
        memory_scan_batch(path, v_id1, v_id2)

    
def memory_scan_batch(path, v_id1, v_id2):
    print "this is memory_scan_batch"
    print 'hello'
    # 随机获取虚拟机的列表
    import os
    import random
    str = os.popen("pidof 'qemu-kvm'").read()
    a = str.split("\n")
    cc = a[0]
    strq = cc.split(" ")
    slice = random.sample(strq, 2)
    #
    os.system("make")
    os.system("rmmod umu.ko")
    os.system("rmmod umu.ko")
    print '开始进行内存的生成'
    os.system("insmod umu.ko pid_from_user=%d log_file='%s/v_id1'" % (v_id1, path[0]))
    os.system("rmmod umu.ko")
    os.system("insmod umu.ko pid_from_user=%d log_file='%s/v_id2'" % (v_id2, path[0]))
    print '内存文件获取完成'    
    # 已经获取所需要的文本，将所需模块卸载
    os.system("make clean")
    os.system("rmmod umu.ko")
    os.system("python text.py")
    mem_quchong(v_id1, v_id2)
    # 将虚拟内存和物理内存映射显示出来
    os.system("rm -rf v_id1")
    os.system("rm -rf v_id2")
    os.system("rm -rf v_final")


def mem_quchong(v_id1, v_id2):
    import os
    import sys
    import re
    import random
    ciku = open(r'v_final', 'r')
    xieci = open(r'v_result', 'a')
# # add code##
    sp = os.popen("ps %d" % (v_id1)).read()
    s1 = re.findall('guest=(.*?),', sp, re.S)
     
    sq = os.popen("ps %d" % (v_id2)).read()
    s2 = re.findall('guest=(.*?),', sq, re.S)

    xieci.writelines("------------------------")
    xieci.writelines("虚拟机:进程号为" + str(v_id1) + " " + "虚拟机名为:" + str(s1) + " " + "和" + "虚拟机:进程号为:" + str(v_id2) + " " + "虚拟机名为:" + str(s2) + "的比较结果如下：")
    xieci.writelines("\n")

    cikus = ciku.readlines()
    list2 = {}.fromkeys(cikus).keys()
    i = 1
    for line in list2:
        if line[0] != ',':
            i += 1
            xieci.writelines(line)
    # 写入分隔字符
    xieci.writelines("\n")
    xieci.close()



if __name__ == '__main__':
    print memory_scan()








