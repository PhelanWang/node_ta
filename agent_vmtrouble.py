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


@agent.entry("blue_screen", version="1.0.1")
def blue_screen(subtask_id, args):
    from vm_trouble.vm_trouble import execute_test
    before_data, after_data = execute_test()
    result = '启动两台虚拟机后，信息如下:\n' + before_data + \
             '\n一台虚拟机故障后，信息如下:\n' + after_data

    print result
    detail = '测试启动两台虚拟机，获取虚拟机信息，然后模拟一台虚拟机崩溃，再次获取系统信息。\n' \
             '可以从信息中看到，一台虚拟机故障后不会影响另一台虚拟机的正常运行。\n'
    print detail
    agent.post_report(subtask_id,
                      severity=0,
                      result=1,
                      brief='',
                      detail=detail.replace('\n', '</br>'),
                      json_data=result.replace('\n', '</br>'))

# Execute this while run this agent file directly
if not is_load_external():
    agent.run()
    # pass
    # blue_screen(0, 0)