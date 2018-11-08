# coding: utf-8

import os


def is_load_external():
    return globals().has_key('AGENT_LOADER')


if not is_load_external():
    from lib.agent.ctest import SwitchAgent
    agent = SwitchAgent(__name__)


# 主机文件访问控制检测
@agent.entry("host_access_detection", version="1.0.1")
def host_access_controll_detection(subtask_id, args):
    # 使用系统命令，列出根目录的文件访问控制权限
    result = os.popen('ls -lh /').read()
    detail = '列出被测试节点的根目录访问权限，r代表可读，w代表可写，x代表可执行。\n'

    print result
    print detail

    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='',
                      detail=detail,
                      json_data=result.replace('\n', '</br>'))


# 虚拟机访问控制检测
@agent.entry("vm_access_detection", version="1.0.1")
def vm_access_controller_detection(subtask_id, args):
    from access_detection.vm_access_controll_detection import list_access_controll, get_vm_infor
    import time
    time.sleep(5)
    result = list_access_controll(args)
    detail = '列出虚拟机磁盘的根目录访问权限，r代表可读，w代表可写，x代表可执行。\n'
    print result
    print detail

    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='',
                      detail=detail,
                      json_data=result.replace('\n', '</br>'))


# Execute this while run this agent file directly
if not is_load_external():
    # args = {}
    # args['path'] = '/root/PycharmProjects/96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    # vm_access_controller_detection(0, args)
    # host_access_controll_detection(0, args)
    agent.run()