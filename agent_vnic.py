# -*- coding:utf-8 -*-
__author__ = 'root'
import time

def is_load_external():
    return globals().has_key("AGENT_LOADER")

# Execute this while run this agent file directly
if not is_load_external():
    # Import ctest package
    from lib.agent.ctest import SwitchAgent

    # Create SwitchAgent instance
    agent = SwitchAgent(__name__)

# OJBK
@agent.entry("vnic_testing",version="1.0.2")
def vnic_analysis(subtask_id, args):
    from vnic.vnic_analy import VnicTest
    print "vnic test shell run!"
    rpt = {
            "brief":"未能旁路此网卡数据",
            "detail":"未能旁路此网卡数据"
        }
    vt = VnicTest('qemu-kvm', 'vhost')
    ###
    #shut down all vms !!
    type = "未能旁路此网卡数据"
    try:
        vt.shutdown()
        if True == vt.begin():
                #time.sleep(60)
                rpt = vt.stop()
                type = "数据已旁路"
    except:
        rpt["brief"] = "未能旁路此网卡数据"
        rpt["detail"]= "未能旁路此网卡数据"
        type = 'date '
    
    print 'type: ', type, 'rpt: ', rpt['brief'], rpt['detail']
    agent.post_report(subtask_id,
                      severity=1,
                      result=1,
                      brief=rpt["brief"],
                      detail=rpt["detail"],
                      json_data={'vnic_result':type})
    
    #print 'end vnic'
    
# Execute this while run this agent file directly
if not is_load_external():
    print vnic_analysis(0, 0)
    # Run agent
#     agent.run()
    
