# coding: utf-8

import pexpect
import os
import time


def is_load_external():
    return globals().has_key('AGENT_LOADER')


# Execute this while run this agent file directly
if not is_load_external():
    # Import ctest package
    from lib.agent.ctest import SwitchAgent
    # Create SwitchAgent instance
    agent = SwitchAgent(__name__)


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


@agent.entry("blue_screen", version="1.0.1")
def blue_screen():
    get_info()
    print 'start sleep. . .'
    time.sleep(60)
    print 'end sleep. . .'
    get_info()



# Execute this while run this agent file directly
if not is_load_external():
    # agent.run()
    # pass
    blue_screen(0, 0)