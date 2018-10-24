# coding: utf-8

import os


def is_load_external():
    return globals().has_key('AGENT_LOADER')


# Execute this while run this agent file directly
if not is_load_external():
    # Import ctest package
    from lib.agent.ctest import SwitchAgent
    # Create SwitchAgent instance
    agent = SwitchAgent(__name__)


# 主机文件访问控制检测
@agent.entry("host_access_detection", version="1.0.1")
def host_access_controll_detection(subtask_id, args):
    # 使用系统命令，列出根目录的文件访问控制权限
    result = os.system('ls -lh /')

    print result
    return

    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='result of erase_scan',
                      detail='Failed!',
                      json_data={'detail_report': 'Disk status error!'})

# 虚拟机访问控制检测
@agent.entry("vm_access_detection", version="1.0.1")
def vm_access_controller_detection(subtask_id, args):
    from access_detection.vm_access_controll_detection import list_access_controll, get_vm_infor
    # list_access_controll(args)
    get_vm_infor(args)

# Execute this while run this agent file directly
if not is_load_external():
    args = {}
    args['path'] = '/root/PycharmProjects/96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    vm_access_controller_detection(0, args)