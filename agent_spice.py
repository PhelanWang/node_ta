# coding: utf-8
from time import sleep
__author__ = 'Henry'
# Determine whether loaded by agent_loader
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
@agent.entry("spice", version="1.0.1")
def spice(subtask_id, args):
    # Post report to switch server:
    # agent.post_report(subtask_id, severity, result, brief, detail, json_data)
    import os, time, ConfigParser
    from spice_vnc.format_data import get_format_data
    conf = ConfigParser.ConfigParser()
    conf.read('spice_vnc.conf')
    port = conf.get('SPICE', 'port', '5900')
    cmd = 'tshark -i any -n -f "src port '+port+'" -d "tcp.port=='+port+',vnc" -a duration:120 -w data.cap'
    print 'please wait 2 mins,spice is testing...'
    print cmd
    os.system(cmd)
    #time.sleep(120)
    os.system('hexdump -C data.cap > spice.txt')
    #print 'please wait 5 mins,spice is testing...'
    #time.sleep(120)
    print 'begin to anaylyse...'
    #os.system('chmod 777 data.cap')
    #result=os.popen('hexdump -C data.cap')
    file = open('spice.txt')
    result = file.read()
    file.close()
    result = get_format_data(result, 15)
    #print result
    os.system('rm -rf data.cap')
    # json_data is default as None
    for line in result:
        print line
    agent.post_report(subtask_id,
                      severity=0,
                      result=1,
                      brief='SPICE',
                      detail='获取SPICE协议的数据内容，若有明文，则可能部分数据未加密!\n',
                      json_data=result)

# Execute this while run this agent file directly
if not is_load_external():
    # Run agent
    # agent.run()
    # os.system('bash spice/run.sh')
    spice(0, 0)
    
