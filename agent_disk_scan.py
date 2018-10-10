# -*- coding: utf-8 -*-

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
# 扫描磁盘，并比较关键字，检测磁盘是否加密
# nfs 镜像文件路径
# args {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
@agent.entry("disk_scan", version="1.0.2")
def my_disk_scan(subtask_id,args):
    from sec_storage.disk_scan import get_vm_disk_size,symbol_scan
    print 'startup disk_scan'

    vm_disk_path = args["path"]
    vm_disk_size=int(get_vm_disk_size(vm_disk_path))
    print vm_disk_size
    report = symbol_scan(vm_disk_path, vm_disk_size)
    print 'report :', report
    if report == "ERROR,扫描出现未指定错误" or report == "ERROR!无法获取磁盘空间信息":
        agent.post_failure(subtask_id)
    else:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of disk_scan',
                          detail=report["result"],
                          json_data={'detail_report': report["detail"]})

# OK
# 删除文件，并检测是否擦除
# args {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
@agent.entry("erase_scan", version="1.0.2")
def my_erase_scan(subtask_id, args):
    from sec_storage.disk_erase_detect import get_total_save,do_erase_scan
    import os

    print 'startup erase_scan'
    
    disk_path = args["path"]
    result = get_total_save(disk_path)
    
    os.system('rm -rf '+disk_path)
    
    print 'result: ', result
    if result == "ERROR":
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of erase_scan',
                          detail='Failed!',
                          json_data={'detail_report': 'Disk status error!'})
        return    
    report = do_erase_scan()
    
    print 'report: ', report
    if report == "ERROR":
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of erase_scan',
                          detail='Failed!',
                          json_data={'detail_report': 'Disk status error!'})
    else:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of erase_scan',
                          detail=report["result"],
                          json_data={'detail_report': report["detail"]})
 
# OK   
# 保存文件大小到文件中   
# args {'path': '/root/share/c3d4181e-bfda-4c78-bfb6-d7205959db02'}) 
@agent.entry("erase_save", version="1.0.2")
def my_erase_save(subtask_id,args):
    from sec_storage.disk_erase_detect import get_total_save,do_erase_scan
    disk_path = args["path"]
    result = get_total_save(disk_path)
    print "result: ", result
    if result == "ERROR":
        agent.post_failure(subtask_id)
    else:
        #/tmp/cloud_erase_test/
        agent.post_report(subtask_id,
                          severity = 1,
                          result = 0,
                          brief='done',
                          detail="save info succeed")


@agent.entry("cross_memory", version="1.0.1")
def my_cross_memory(subtask_id, args):
    from memory_scan.memory_cross import memory_scan
    report = memory_scan()
    print 'report: ', report
    agent.post_report(subtask_id,
                        severity = 1,
                        result = 0,
                        brief = 'done',
                        detail = report)


@agent.entry("virtual_disk_scan", version="1.0.1")
def my_vdisk_scan(subtask_id, args):
    from vdisk.vdis_scan import virtual_disk_scan
    data = virtual_disk_scan(args)
    agent.post_report(subtask_id,
                        severity = 1,
                        result = 0,
                        brief = 'done',
                        detail = data)

# Execute this while run this agent file directly
if not is_load_external():
    args = {}
    args["path"] = '/root/share/c3d4181e-bfda-4c78-bfb6-d7205959db02'
    args["name"]  = 'c3d4181e-bfda-4c78-bfb6-d7205959db02'
#     print 'report: ', my_disk_scan(0, {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
#     my_erase_scan(0, {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})

#     my_erase_save(0, {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
#     my_disk_scan(0, args)
#     my_erase_scan(0, args)
#     my_cross_memory(0, 0)
    my_vdisk_scan(0, args)
    # Run agent
#     agent.run()

