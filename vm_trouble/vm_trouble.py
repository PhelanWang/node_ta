# coding: utf-8
import os
import pexpect, time


# 修改/etc/libvirt/qemu.conf文件，设置根权限
def modify_to_root():
    flag = 0
    with open('/etc/libvirt/qemu.conf', 'rw+') as file:
        data = file.read()
        if data.find('#user') == -1 and data.find('#group') == -1:
            return True
        else:
            data = data.replace('#user', 'user').replace('#group', 'group')
        file.seek(0, 0)
        file.truncate()
        file.write(data)
    os.system('service libvirtd restart')


def execute_command(cmd):
    print cmd
    child = pexpect.spawn(cmd)
    child.sendline('admin')
    child.sendline('admin')
    return child


# 获取虚拟机信息
def get_info():
    child = execute_command('virsh list')
    for line in child.readlines():
        print line

    result = child.readlines()[4:-1]
    vms_info = []
    for line in result:
        line_list = list(set(line.strip(' \r\n').split(' ')))
        line_list.sort()
        vms_info.append(line_list)
        print line_list

    for vm_info in vms_info:
        child = execute_command('virsh dommemstat %s' % vm_info[1])
        result = child.readlines()[2:]
        result = reduce(lambda a, b: a + b, map(lambda s: s.replace('\r\n', '\n'), result), '虚拟机名称: %s\n虚拟机信息:\n' % vm_info[2])
        print result

    hypervisor_info = 'hypervisor结果如下:\n'
    hyper_infor = os.popen('free -m').read()
    print hyper_infor

# 将cirrosx.xml中的IMAGE_PATH替换为正确路径
def replace_image_path(file_path):
    file = open(file_path, 'rw+')
    # cirros_path = os.getcwd() + '/vm_trouble/cirros-disk.img'
    cirros_path = os.getcwd() + '/cirros-disk.img'
    lines = file.readlines()
    for index in range(0, len(lines)):
        if 'source file' in lines[index]:
            lines[index] = '            ' \
                           '<source file=' \
                           '"'+cirros_path+'"' \
                           '/>\n'
            break
    file.seek(0, 0)
    file.truncate()
    file.writelines(lines)
    print 'replace path ok. . .'

# 启动cirros1和cirros2两台虚拟机
def start_vms():
    # cirros_path = os.getcwd() + '/vm_trouble'
    cirros_path = os.getcwd()
    execute_command('virsh define %s' % cirros_path+'/cirros1.xml')
    execute_command('virsh define %s' % cirros_path+'/cirros2.xml')
    execute_command('virsh start cirros1')
    time.sleep(3)
    execute_command('virsh start cirros2')
    time.sleep(3)
    get_info()


replace_image_path('cirros1.xml')
replace_image_path('cirros2.xml')
modify_to_root()
start_vms()



