# coding: utf-8

import os

# 将 vdisk 文件夹中的 qemu-kvm 替换到 /usr/libexec/qemu-kvm
# 将 /usr/libexec/qemu-kvm 备份为 /usr/libexec/qemu-kvm.back
# 以便旁路出文件数据
def replace_qemu_kvm():
    current_path = os.getcwd() + '/vdisk'
    system_qemu_path = '/usr/libexec'
    result = os.system('mv ' + system_qemu_path + '/qemu-kvm ' + system_qemu_path + '/qemu-kvm.back')
    print result
    result = os.system('cp ' + current_path + '/qemu-kvm ' + system_qemu_path + '/qemu-kvm')
    print result

# 将系统原有 qemu-kvm 还原
# 即将 /usr/libexec/qemu-kvm.back 还原为 /usr/libexec/qemu-kvm
def disreplace_qemu_kvm():
    system_qemu_path = '/usr/libexec'
    result = os.system('mv ' + system_qemu_path + '/qemu-kvm.back ' + system_qemu_path + '/qemu-kvm')
    print result


# 分析文件中的关键字
def virtual_disk_scan(args):
    import os
    import time



    keyword = args['keyword']
    data = ''
    if keyword == '':
        keyword = ''
    # keyword=u'经济 15% 南洋科技'
    m_list = keyword.split(' ')
    # print m_list
    s = ''
    # 拼接关键字
    for item in m_list:
        s += item + ' '

    if not os.path.exists("/home/qemu/"):
        os.mkdir("/home/qemu/")
        os.system("chown qemu /home/qemu")
        os.system("chmod 777 /home/qmeu")

    root = '/blk/virtio_blk'

    current_path = os.getcwd()

    error = os.system(current_path + root + '/run.sh ' + '/home/qemu/virtio_blk.log ' + s)

    num = len(m_list)  # 关键字个数

    if not error:
        while num:
            for filename in m_list:
                filepath = '/tmp/virtio_blk/' + filename + '.txt'
                if os.path.exists(filepath):
                    num -= 1
                    # 说明文件个数不够，继续等待知道文件个数和m_list长度大小一致
            print num
            if num:
                num = len(m_list)
                # 睡眠1秒在查找
                time.sleep(1)

                # 此时文件必定以及全部存在
        for filename in m_list:
            filepath = '/tmp/virtio_blk/' + filename + '.txt'
            fo = open(filepath)
            try:
                data += fo.read() + '\n'
            finally:
                fo.close()
        print 'data:', data.replace('[.:,;\\]', '')
        return xmlrpclib.Binary(data.replace('[.:,;\\]', ''))
    else:
        print 'error'
        return xmlrpclib.Binary('error')