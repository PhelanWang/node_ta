# -*- coding: utf-8 -*-
from numpy.dual import det

__author__ = 'Henry'

def is_load_external():
    return globals().has_key('AGENT_LOADER')

# Execute this while run this agent file directly
if not is_load_external():
    # Import ctest package
    from lib.agent.ctest import SwitchAgent

    # Create SwitchAgent instance
    agent = SwitchAgent(__name__)


# Register function "my_openvas" on service "openvas"


# OK
# 对于同一个磁盘mount两个会出错，尝试只启动一台
# 格式修改完成
@agent.entry("mmount", version="1.0.2")
def mmount_test(subtask_id, args):
    from virus_scan.mount import Mounter
    disk_path = ''
    disk_name = ''
    disk_type = ''
    print args
    try:
        disk_path = args["path"]
        disk_name = args["name"]
        # disk_type = args["type"]
    except:
        print "can't get args!"
        
    mt = Mounter(disk_path, disk_name)
    # print 'start mounting...'
    # mount = mt.mount()
    report = mt.getReport()
    rpt=''
    detail=''
    brief=''
    print '---------------'
    print report
    print '---------------'

    if report == False:
        rpt = '启动虚拟机失败，该磁盘不可引导或未初始化。\n'
        brief = '启动虚拟机失败。\n'
        detail = '该磁盘不可引导或未初始化。\n'
    else:
        brief = '成功启动虚拟机'
        detail = '对于同一个磁盘，尝试对该磁盘启动两个虚拟机。\n'
        rpt = report

    print '----'
    print detail
    print '----'
    agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief=brief,
                          detail=detail,
                          json_data=report)


# Execute this while run this agent file directly
if not is_load_external():
    # Run agent
    args = {}
    args["path"] = '/root/PycharmProjects/96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    args["name"] = '96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    mmount_test(0, args)
    # agent.run()
