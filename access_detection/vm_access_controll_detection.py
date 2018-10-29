# coding: utf-8

import os


# 将虚拟磁盘挂在到 /mnt目录下
def mount_disk(args):
    mod_path = os.getcwd() + '/access_detection/nbd.ko'
    os.system('insmod ' + mod_path + ' max_part=16')
    os.system('qemu-nbd -c /dev/nbd0 ' + args['path'])
    os.system('mount /dev/nbd0p1 /mnt')


def umount_disk():
    os.system('umount /mnt')
    os.system('qemu-nbd --disconnect /dev/nbd0')


# 使用linux命令虚拟机磁盘，然后返回根目录下的文件的访问控制权限
def list_access_controll(args):
    mount_disk(args)
    result = os.system('ls -lh /mnt')
    umount_disk()
    return result


# 获取虚拟机的版本信息
def get_vm_infor(args):
    mount_disk(args)
    result = '虚拟机系统内核名称: '
    kernal_name = os.popen('/mnt/bin/uname -s').read()
    result += kernal_name
    result += '虚拟机主机名称: '
    result += os.popen('/mnt/bin/uname -n').read()
    result += '虚拟机内核发行号: '
    version = os.popen('/mnt/bin/uname -r').read()
    result += version
    result += '虚拟机架构: '
    result += os.popen('/mnt/bin/uname -i').read()
    result += '虚拟机操作系统版本: '
    result += os.popen('cat /mnt/etc/issue').read()
    umount_disk()
    print result
    print version.split('-')[0]
