# coding: utf-8

import pexpect
import os


# 获取虚拟机信息
def get_info():
    child = pexpect.spawn('virsh list --all')
    child.sendline('admin')
    child.sendline('admin')
    result = child.readlines()[4:-1]
    vms_info = []
    for line in result:
        line_list = list(set(line.strip(' \r\n').split(' ')))
        line_list.sort()
        vms_info.append(line_list)
        print line_list

    for vm_info in vms_info:
        child = pexpect.spawn('virsh dommemstat %s' % vm_info[1])
        child.sendline('admin')
        child.sendline('admin')
        result = child.readlines()[2:]
        result = reduce(lambda a, b: a + b, map(lambda s: s.replace('\r\n', '\n'), result), '虚拟机名称: %s\n虚拟机信息:\n' % vm_info[2])
        print result

    hypervisor_info = 'hypervisor结果如下:\n'
    hyper_infor = os.system('free -m')
    print hyper_infor


def blue_screen():
    child = pexpect.spawn('virsh list --all')
    child.sendline('admin')
    child.sendline('admin')
    result = child.readlines()[4:-1]
    vms_info = []
    for line in result:
        line_list = list(set(line.strip(' \r\n').split(' ')))
        line_list.sort()
        vms_info.append(line_list)
        print line_list

    for vm_info in vms_info:
        child = pexpect.spawn('virsh dommemstat %s' % vm_info[1])
        child.sendline('admin')
        child.sendline('admin')
        result = child.readlines()[2:]
        result = reduce(lambda a, b: a + b, map(lambda s: s.replace('\r\n', '\n'), result), '虚拟机名称: %s\n虚拟机信息:\n' % vm_info[2])
        print result

    hypervisor_info = 'hypervisor结果如下:\n'
    hyper_infor = os.system('free -m')
    print hyper_infor




blue_screen()
