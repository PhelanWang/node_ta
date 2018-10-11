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
    mount = mt.mount()
    report = mt.getReport()
    rpt=''
    detail=''
    brief=''
    print report
    
    if(report==False):
            rpt='启动虚拟机失败，该磁盘不可引导或未初始化'
            brief='启动虚拟机失败'
            detail='该磁盘不可引导或未初始化'
    else:
        brief ='成功启动虚拟机'
        detail=report
        rpt=report
    print 'report:', rpt
    agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief=brief,
                          detail=detail,
                          json_data={'mm_result': rpt})




# Execute this while run this agent file directly
if not is_load_external():
    # Run agent
    # args = {}
    # args["path"] = '/root/share/c3d4181e-bfda-4c78-bfb6-d7205959db02'
    # args["name"]  = 'c3d4181e-bfda-4c78-bfb6-d7205959db02'
    # mmount_test(0, args)
    agent.run()
