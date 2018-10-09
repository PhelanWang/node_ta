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
    import os
    import time

    keyword = args['keyword']
    data = ''
    if keyword == '':
        keyword = ''
    # keyword=u'经济 15% 南洋科技'
    m_list = keyword.split(' ')
    # print m_list
    s = ''
    # 拼接关键字
    for item in m_list:
        s += item + ' '

    if not os.path.exists("/home/qemu/"):
        os.mkdir("/home/qemu/")
        os.system("chown qemu /home/qemu")
        os.system("chmod 777 /home/qmeu")

    root = '/blk/virtio_blk'

    current_path = os.getcwd()

    error = os.system(current_path + root + '/run.sh ' + '/home/qemu/virtio_blk.log ' + s)

    num = len(m_list)  # 关键字个数

    if not error:
        while num:
            for filename in m_list:
                filepath = '/tmp/virtio_blk/' + filename + '.txt'
                if os.path.exists(filepath):
                    num -= 1
                    # 说明文件个数不够，继续等待知道文件个数和m_list长度大小一致
            print num
            if num:
                num = len(m_list)
                # 睡眠1秒在查找
                time.sleep(1)

                # 此时文件必定以及全部存在
        for filename in m_list:
            filepath = '/tmp/virtio_blk/' + filename + '.txt'
            fo = open(filepath)
            try:
                data += fo.read() + '\n'
            finally:
                fo.close()
        print 'data:', data.replace('[.:,;\\]', '')
        return xmlrpclib.Binary(data.replace('[.:,;\\]', ''))
    else:
        print 'error'
        return xmlrpclib.Binary('error')


# Execute this while run this agent file directly
if not is_load_external():
    args = {}
    args["path"] = '/root/share/c3d4181e-bfda-4c78-bfb6-d7205959db02'
    args["name"]  = 'c3d4181e-bfda-4c78-bfb6-d7205959db02'
#     print 'report: ', my_disk_scan(0, {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
#     my_erase_scan(0, {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})

#     my_erase_save(0, {'path': '/root/share/cb7e72a4-b396-4e24-bbb2-717e0bf62e49/images/cdab97a6-da5e-4103-aa24-9d9cf84440e3/7b2465ac-d3b2-4a79-b384-2c73bfb27521'})
#     my_disk_scan(0, args)
    my_erase_scan(0, args)
#     my_cross_memory(0, 0)
    # Run agent
#     agent.run()

