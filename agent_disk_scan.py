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
# 格式检测完成
# args {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
@agent.entry("disk_scan", version="1.0.1")
def my_disk_scan(subtask_id,args):
    from sec_storage.disk_scan import get_vm_disk_size,symbol_scan
    print 'startup disk_scan'
    vm_disk_path = args["path"]
    vm_disk_size=int(get_vm_disk_size(vm_disk_path))
    print vm_disk_size
    report = symbol_scan(vm_disk_path, vm_disk_size)
    print 'report :', report

    if report == "磁盘错误, 扫描出现未指定错误!" or report == "磁盘错误, 无法获取磁盘空间信息!":
        detail = report + "请检测磁盘路径是否正确。"
    else:
        detail = report['result']
        report = report['detail']

    print detail
    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='result of disk_scan',
                      detail=detail,
                      json_data=report)

# OK
# 删除文件，并检测是否擦除
# args {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
# 格式修改完成
@agent.entry("erase_scan", version="1.0.1")
def my_erase_scan(subtask_id, args):
    from sec_storage.disk_erase_detect import get_total_save, do_erase_scan
    import os

    print 'startup erase_scan'
    
    disk_path = args["path"]
    result = get_total_save(disk_path)
    
    # os.system('rm -rf '+disk_path)
    
    print 'result: ', result
    if result == "ERROR":
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of erase_scan',
                          detail='进行磁盘扫描失败。\n',
                          json_data="进行指定磁盘扫描失败，请检查给定路径是否正确。\n")
        return    
    report = do_erase_scan()
    print report

    if report == None:
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of erase_scan',
                          detail='进行磁盘扫描失败。\n',
                          json_data="进行指定磁盘扫描失败，请检查给定路径是否正确。\n")
    else:
        print report['result'], report['detail']
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='result of erase_scan',
                          detail=report['detail'],
                          json_data=report['result'])
 
# OK   
# 保存文件大小到文件中   
# args {'path': '/root/share/c3d4181e-bfda-4c78-bfb6-d7205959db02'}) 
@agent.entry("erase_save", version="1.0.1")
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

# 格式修改完成
@agent.entry("cross_memory", version="1.0.1")
def my_cross_memory(subtask_id, args):
    import os
    from memory_scan.memory_cross import memory_scan
    (report, state) = memory_scan()
    if not state:
        detail = '运行测试功能失败!'
    else:
        detail = '运行测试功能成功!'
        if report == []:
            detail += '\n未发现交叉内存页面!'
        else:
            detail += '\n发现交叉内存页面，显示部分交叉页面地址如下:\n' \
                      '若要显示所有交叉的内存页面地址，查看节点上文件，路径为：' + os.getcwd() + '/memory_scan_umuery/v_result'
    print detail, '\n', report
    agent.post_report(subtask_id,
                        severity = 1,
                        result = 0,
                        brief = 'done',
                        detail = detail,
                        json_data=report)

# 格式修改完成
@agent.entry("virtual_disk_scan", version="1.0.1")
def my_vdisk_scan(subtask_id, args):
    from vdisk.vdis_scan import virtual_disk_scan

    args = {}
    args['keyword'] = ['ovirt-test', 'cloud-platforms', 'virtual-scan', 'data-isolate']

    data = virtual_disk_scan(args)

    detail = '启动虚拟机后在任意文件中写入内容，如果如果内容中有' + reduce(lambda a, b: a+', '+b, args['keyword'], '') + \
             '等关键字，测试功能将会把相关的数据旁路出来。'
    print data
    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='done',
                      detail=data,
                      json_data=data)

# Execute this while run this agent file directly
if not is_load_external():
    args = {}
    args["path"] = '/root/PycharmProjects/cp/1fe0032b-aabd-4315-8390-6bbac5844ea5'
    args["name"] = '1fe0032b-aabd-4315-8390-6bbac5844ea5'

    # args['path'] = '/root/PycharmProjects/96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    # args['name'] = '96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    # my_disk_scan(0, args)
    # my_erase_scan(0, args)
    # my_cross_memory(0, 0)
    # my_vdisk_scan(0, args)
    # Run agent
    # agent.run()

