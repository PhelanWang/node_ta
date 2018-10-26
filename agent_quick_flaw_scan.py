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
@agent.entry("quick_kvmflaw_scan", version="1.0.1")
def my_quick_kvmflaw_scan(subtask_id,args):
    from quick_flaw_scan.ShowInfoOfScankvm_flaw import getFlawInfoBySql
    virus_table = "select * from kvm_flaw_scan"
    # 此处的report返回一个包含所有kvm漏洞信息的列表
    report = getFlawInfoBySql(virus_table)
    if report == []:
        detail = '在此系统中没有发现QEMU-KVM漏洞'
    else:
        detail = 'QEMU-KVM漏洞：根据系统环境，扫描系统列出系统中可能存在的QEMU-KVM漏洞'
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_kvmflaw_scan',
                          detail=detail,
                          json_data=report)

# OK
# http://192.168.1.117:9000/switch/agent/quick_ovirtflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_ovirtflaw_scan", version="1.0.1")
def my_quick_ovirtflaw_scan(subtask_id,args):
    from quick_flaw_scan.ShowInfoOfScanOvirt_flaw import getFlawInfoBySql
    print 'startup quick_ovirtflaw_scan'
    # 此处的report返回一个包含所有Ovirt漏洞信息的列表
    report = getFlawInfoBySql("select * from Ovirt_flaw_scan")
    if report == []:
        detail = '在此系统中没有发现oVirt漏洞'
    else:
        detail = 'oVirt漏洞：根据系统环境，扫描系统列出系统中可能存在的oVirt漏洞'
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_kvmflaw_scan',
                          detail=detail,
                          json_data=report)

# http://192.168.1.117:9000/switch/agent/quick_libvirtflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_libvirtflaw_scan", version="1.0.1")
def my_quick_libvirtflaw_scan(subtask_id, args):
    from quick_flaw_scan.ShowInfoOfScanlibvirt_flaw import getFlawInfoBySql
    # 此处的report返回一个包含所有libvirt漏洞信息的列表
    report = getFlawInfoBySql("select * from libvirt_flaw_scan")
    if report == []:
        detail = '在此系统中没有发现libvirt漏洞'
    else:
        detail = 'libvirt漏洞：根据系统环境，扫描系统列出系统中可能存在的libvirt漏洞'


        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_kvmflaw_scan',
                          detail=detail,
                          json_data=report)
                          

# OK
# http://192.168.1.117:9000/switch/agent/quick_VDSMflaw_scan
# args = '' or None
# version = '1.0.2'
@agent.entry("quick_VDSMflaw_scan", version="1.0.1")
def my_quick_VDSMflaw_scan(subtask_id,args):
    from quick_flaw_scan.ShowInfoOfScanVDSM_flaw import getFlawInfoBySql
    report = getFlawInfoBySql("select * from VDSM_flaw_scan")#此处的report返回一个包含所有VDSM漏洞信息的列表
    if report == []:
        detail = '在此系统中没有发现VDSM漏洞'
    else:
        detail = 'VDSM漏洞：根据系统环境，扫描系统列出系统中可能存在的VDSM漏洞'

        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of quick_kvmflaw_scan',
                          detail=detail,
                          json_data=report)



# Execute this while run this agent file directly
if not is_load_external():
    # my_quick_VDSMflaw_scan(0, 0)
    # my_quick_libvirtflaw_scan(0, 0)
    my_quick_ovirtflaw_scan(0, 0)
    # my_quick_kvmflaw_scan(0, 0)
    # Run agent
    # agent.run()

# 格式修改完成