# -*- coding:utf-8 -*-



# Determine whether loaded by agent_loader
def is_load_external():
    return globals().has_key('AGENT_LOADER')
# Execute this while run this agent file directly
if not is_load_external():
    # Import ctest package
    from lib.agent.ctest import SwitchAgent

    # Create SwitchAgent instance
    agent=SwitchAgent(__name__)


# Register function "my_openvas" on service "openvas"

# OJBK
# 没有抓到数据
@agent.entry("unsecurity_service_testing", version="1.0.1")
def my_unsecurity_service_testing(subtask_id,args):
    from lib.agent.ctest import SwitchAgent
    import threading
    from threading import Thread
    from sec_network import client as cli
    from sec_network import unsecurity_service as unsecurity
    import time
    from sec_network.pyTimer import Pysettimer

    # Get value of global K-V database item "engine-ip". see get_global(), set_global()
    #engine_ip=agent.get_global("engine-ip")

#     client=Pysettimer(cli.sendmessage, "Hello World")
    
    #---\
    capture=Pysettimer(unsecurity.capture, 'test')
    #---/
    
#     client.setDaemon(True)
#     client.start()
#     time.sleep(10)
    
    #----\
    capture.start()
    capture.join()
    #----/
    # Post report to switch server:
    # agent.post_report(subtask_id, severity, result, brief, detail, json_data)
    # json_data is default as None

    if(unsecurity.get_captured()):
        print unsecurity.getfilterpackupd()
        agent.post_report(subtask_id,
                          severity=1,
                          result=0,
                          brief='String Match Successful! ',
                          detail='The message send to the server is captured',
                          json_data={
                              "method": "在ovirt云平台的两个node结点上部署两台虚拟机,分别为vm1和vm2,在vm1中部署一个不安全的服务,发送端部署在vm2中,使用wireshark抓包工具,在发送端或者接收端网卡上抓取数据,以验证云平台的安全性",
                              "config": "系统要求:\nfedora19+,centos7.0+（kernel支持kvm）\nwireshark-1.10.13-1.fc20.x86_64,ovirt平台,至少一个node节点，一个虚拟机",
                              "logs": [
                                    {"type": "text", "content": unsecurity.getfilterpackupd()}
                                ],
                              "conclusions": [{"type": "text", "content": "The data  is captured."}]
                          })
    else:
        print 'else'
        agent.post_report(subtask_id,
                          severity=1,
                          result=1,
                          brief='String Match failed',
                          detail='The message send to the server cannot captured',
                          json_data={
                              "method": "在ovirt云平台的两个node结点上部署两台虚拟机,分别为vm1和vm2,在vm1中部署一个不安全的服务,发送端部署在vm2中,使用wireshark抓包工具,在发送端或者接收端网卡上抓取数据,以验证云平台的安全性",
                              "config": "系统要求:\nfedora19+,centos7.0+（kernel支持kvm）\nwireshark-1.10.13-1.fc20.x86_64,ovirt平台,至少一个node节点，一个虚拟机",
                              "logs": [
                                    {"type": "text", "content":'The data cannot be captured'}
                                ],
                              "conclusions": [{"type": "text", "content": "The data cannot be captured"}]
                          })


# Execute this while run this agent file directly
if not is_load_external():
    # my_unsecurity_service_testing(0, 0)
    # Run agent
    agent.run()
