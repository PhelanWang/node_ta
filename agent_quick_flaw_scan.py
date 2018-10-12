# -*- coding: utf-8 -*-

__author__ = 'root'

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
# http://192.168.1.117:9000/switch/agent/quick_kvmflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_kvmflaw_scan", version="1.0.2")
def my_quick_kvmflaw_scan(subtask_id,args):
    from quick_flaw_scan.ShowInfoOfScankvm_flaw import getFlawInfoBySql
    print 'startup quick_kvmflaw_scan'
    print 'args is: ', args

    virus_table = "select * from kvm_flaw_scan"
    #vm_disk_size=int(get_vm_disk_size(vm_disk_path))
    #print vm_disk_size
    report = getFlawInfoBySql(virus_table)#此处的report返回一个包含所有kvm漏洞信息的列表
    if report == None:
        agent.post_failure(subtask_id)
    #下面的部分还不知道该怎么改
    print report
    ret=''
    for s in report:
        ret+=s;
    else:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_kvmflaw_scan',
                          detail='Test KVM',
                          json_data={'detail_report': ret})

# OK
# http://192.168.1.117:9000/switch/agent/quick_ovirtflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_ovirtflaw_scan", version="1.0.2")
def my_quick_ovirtflaw_scan(subtask_id,args):
    from quick_flaw_scan.ShowInfoOfScanOvirt_flaw import getFlawInfoBySql
    print 'startup quick_ovirtflaw_scan'
    report = getFlawInfoBySql("select * from Ovirt_flaw_scan")#此处的report返回一个包含所有Ovirt漏洞信息的列表
    
    ret=''
    for s in report:
        ret+=s;
    
    print report
    if report == None:
        agent.post_failure(subtask_id)
    else:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_ovirtflaw_scan',
                          detail='Test Ovirt',
                          json_data={'detail_report': ret})

# http://192.168.1.117:9000/switch/agent/quick_libvirtflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_libvirtflaw_scan", version="1.0.2")
def my_quick_libvirtflaw_scan(subtask_id, args):
    from quick_flaw_scan.ShowInfoOfScanlibvirt_flaw import getFlawInfoBySql
    report = getFlawInfoBySql("select * from libvirt_flaw_scan")#此处的report返回一个包含所有libvirt漏洞信息的列表
    print report
    ret=''
    for s in report:
        ret += s
    if report == None:
        agent.post_failure(subtask_id)
    else:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='Test libvirt',
                          detail='Test libvirt',
                          json_data={'detail_report':ret})
                          

# OK
# http://192.168.1.117:9000/switch/agent/quick_VDSMflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_VDSMflaw_scan", version="1.0.2")
def my_quick_VDSMflaw_scan(subtask_id,args):
    from quick_flaw_scan.ShowInfoOfScanVDSM_flaw import getFlawInfoBySql
    report = getFlawInfoBySql("select * from VDSM_flaw_scan")#此处的report返回一个包含所有VDSM漏洞信息的列表
    ret=''
    for s in report:
        ret+=s;
    
    print 'value: ', ret
    if report == None:
        agent.post_failure(subtask_id)
    else:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_VDSMflaw_scan',
                          detail='Test VDSM',
                          json_data={'detail_report': ret})



# Execute this while run this agent file directly
if not is_load_external():
    my_quick_VDSMflaw_scan(0, 0)
    my_quick_libvirtflaw_scan(0, 0)
    my_quick_ovirtflaw_scan(0, 0)
    my_quick_kvmflaw_scan(0, 0)
    # Run agent
    # agent.run()

