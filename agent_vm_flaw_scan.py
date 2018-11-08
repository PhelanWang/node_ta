# coding: utf-8


def is_load_external():
    return globals().has_key('AGENT_LOADER')


if not is_load_external():
    from lib.agent.ctest import SwitchAgent
    agent = SwitchAgent(__name__)


@agent.entry("vm_flaw_scan", version='1.0.1')
def vm_flaw_scan(subtask_id, args):
    from access_detection.vm_access_controll_detection import get_vm_infor, version_comapre
    import sqlite3, re
    # args = {'path': '/root/PycharmProjects/96d9b1b5-2f45-4baf-8462-5a166c87a3bb',
    #         'name': '96d9b1b5-2f45-4baf-8462-5a166c87a3bb'}
    json_data = []
    infor, version = get_vm_infor(args)
    version = '.'.join(version.split('.')[:2])

    conn = sqlite3.connect('data/vm_flaw.db')
    c = conn.cursor()
    result = c.execute('SELECT TITLE, DETAIL, IMPACT_PRODUCT FROM FLAW_TABLE').fetchall()
    for line in result:
        item = {}
        item['bugName'] = line[0]
        item['bugInfo'] = line[1]
        if 'Linux Kernel' in line[2]:
            flaw_version = re.findall(r'([0-9].[0-9])', line[2])
            if flaw_version and version_comapre(flaw_version[0], version):
                json_data.append(item)

    print json_data
    agent.post_report(subtask_id,
                      severity=0,
                      result=1,
                      brief='',
                      detail='获取虚拟机系统信息:\n'+infor,
                      json_data=json_data)


if not is_load_external():
    # my_unsecurity_service_testing(0, 0)
    # Run agent
    agent.run()
