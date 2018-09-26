# coding: utf-8
# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: /root/git/ovirt/engine_ta/sec_storage/disk_erase_detect.py
# Compiled at: 2016-05-23 10:39:39

__author__ = 'wz'
import os, random, ConfigParser
disk_belong_root_dic = '/'

def get_mount_point():
    global disk_belong_root_dic
    conf = ConfigParser.ConfigParser()
    conf.read('lib.agent.ctest.conf')
    try:
        disk_belong_root_dic = conf.get('disk', 'path')
    except:
        pass

    info = os.popen('df -hl %s' % disk_belong_root_dic).read().split('\n')
    mount_info = info[1].split(' ')
    mount_point = mount_info[0]
    return mount_point


def get_disk_dir(disk_path):
    if disk_path == '':
        return ''
    for i in range(-1, -len(disk_path), -1):
        if disk_path[i] == '/':
            vm_disk_dir = disk_path[:i]
            break

    return vm_disk_dir


def get_target_disk_path(vm_disk_dir):
    if vm_disk_dir == '':
        return ''
    file_list = os.popen('ls -l %s' % vm_disk_dir).read().split('\n')
    b = len(file_list) / 3
    disk_list = []
    for i in range(0, len(file_list) / 3):
        a = file_list[3 * i + 1].split(' ')
        disk_list.append(a[-1])

    for i in range(0, len(disk_list)):
        disk_list[i] = vm_disk_dir + '/' + disk_list[i]

    return disk_list


def get_file_root_node_list(vm_disk_path_list):
    root_node_list = []
    for i in range(0, len(vm_disk_path_list)):
        info = os.popen('ls -ila %s' % vm_disk_path_list[i]).read().split(' ')
        root_node_list.append(info[0])

    return root_node_list


def get_block_list(node):
    node_info = os.popen("xfs_db -c 'inode %s' -c p -r %s" % (node, get_mount_point())).read().split('\n')
    core_format = node_info[3][14]
    # 获取挂载点信息，core.format磁盘格式
    dict_block = {}
    if core_format == '2':
        a = node_info[43].split(':')
        extent_num_recs = node_info[20][16:]
        for i in range(0, int(extent_num_recs)):
            b = a[i + 1].split(',')
            c = b[1]
            dict_block[c] = b[2]

    if core_format == '3':
        tree_level = node_info[43][15]
        tree_num_recs = node_info[44][17:]
        a = node_info[46].split(':')
        for i in range(0, int(tree_num_recs)):
            b = a[i + 1].split(' ')
            c = get_tree_block(int(b[0]))
            dict_block = dict(dict_block, **c)

    return dict_block


def get_tree_block(block):
    block_info = os.popen("xfs_db -c 'fsblock %s' -c 'type bmapbta' -c p -r %s" % (int(block), get_mount_point())).read().split('\n')
    tree_level = block_info[1][8]
    tree_num_recs = block_info[2][10:]
    block_dict = {}
    if int(tree_level) > 0:
        a = block_info[6].split(':')
        block_ptr_list = []
        for i in range(0, int(tree_num_recs)):
            b = a[i + 1].split(' ')
            block_ptr_list.append(b[0])

        for block_num in block_ptr_list:
            temp = get_tree_block(int(block_num))
            block_dict = dict(block_dict, **temp)

    else:
        if int(tree_level) == 0:
            a = block_info[5].split(':')
            block_recs = []
            for i in range(0, int(tree_num_recs)):
                b = a[i + 1].split(',')
                c = b[1]
                block_dict[c] = b[2]

        else:
            print 'ERROR block infomation'
    return block_dict


def get_scan_block(block, num):
    return int(block) + random.randint(0, int(num) - 1)


def block_compare(block):
    block_info_after = os.popen("xfs_db -c 'fsblock %s' -c 'type text' -c p -r %s" % (block, get_mount_point())).read()
    block_info_before = os.popen('cat /tmp/cloud_erase_test/%s' % block).read()
    if cmp(block_info_before, block_info_after) == 0:
        os.system('rm -rf /tmp/cloud_erase_test/%s' % block)
        return True
    return False


def block_save(block):
    f = open('/tmp/cloud_erase_test/%s' % block, 'w')
    a = os.popen("xfs_db -c 'fsblock %s' -c 'type text' -c p -r %s" % (int(block), get_mount_point())).read()
    f.write(a)
    f.close()


def block_record(dict_block):
    if not os.path.exists('/tmp/cloud_erase_test'):
        os.system('mkdir /tmp/cloud_erase_test')
    r = open('/tmp/cloud_erase_test/list', 'a+')
    a = 0
    for key in dict_block:
        scan_block = get_scan_block(key, dict_block[key])
            #保存到文件中 挂在点到文件中
        block_save(scan_block)
        r.write(str(scan_block) + '\n')
        a += 1
        print scan_block
        print a
        if a == 10:
            break

    r.close()


def get_total_save(disk_path):
    if os.path.exists('/tmp/cloud_erase_test'):
        os.system('rm -rf /tmp/cloud_erase_test')
    try:
        vm_disk_dir = get_disk_dir(disk_path)
        print vm_disk_dir
        vm_disk_path_list = get_target_disk_path(vm_disk_dir)
        print vm_disk_path_list
        if vm_disk_path_list == '':
            return 'ERROR'
        root_node_list = get_file_root_node_list(vm_disk_path_list)
        for node in root_node_list:
            b = get_block_list(node)
            block_record(b)

        return 'DONE'
    except Exception as e:
        print e
        return 'ERROR'


def do_erase_scan():
    detail = "<font size='5'>start erase scanning:</font>"
    is_erased = False
    s = os.popen('cat /tmp/cloud_erase_test/list').read().split('\n')[0:-1]
    for item in s:
        i = block_compare(item)
        detail += '<br>block ' + str(s.index(item) + 1)
        detail += '<br>' + item
        if i:
            detail += '<br>matching succeed'
        else:
            is_erased = True
            detail += '<br>matching failed'
            break

    if is_erased:
        result = 'the disk is ERASED'
    else:
        result = 'the disk is NOT ERASED'
        return {'result': result, 'detail': detail}


if __name__ == '__main__':
    disk_path = u'/home/kvm/images/ee43aa37-1f5b-4664-8ca2-d447afabdf8b/images/ac1fb6ed-2a6e-49ef-8a80-d9240da48dc4/b88c955b-2b8d-4064-a1ad-ab48367e982f'
    get_total_save(disk_path)