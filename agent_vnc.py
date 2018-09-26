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
@agent.entry("vnc", version="1.0.2")
def vnc(subtask_id, args):
    # Post report to switch server:
    # agent.post_report(subtask_id, severity, result, brief, detail, json_data)
    import os,time,ConfigParser
    conf=ConfigParser.ConfigParser()
    conf.read('spice_vnc.conf')
    port=conf.get('VNC', 'port','5900')
    cmd='tshark -i any -n -f \"src port '+port+'\" -d \"tcp.port=='+port+',vnc\" -a duration:120 -w vnc.cap'
    print 'please wait 2 mins,spice is testing...'
    print cmd
    os.system(cmd)
    #time.sleep(120)
    os.system('hexdump -C vnc.cap > vnc.txt')
    #print 'please wait 5 mins,spice is testing...'
    #time.sleep(120)
    print 'begin to anaylyse...'
    #os.system('chmod 777 data.cap')
    #result=os.popen('hexdump -C data.cap')
    file=open('vnc.txt')
    result=file.read()
    file.close()
    #print result
    os.system('rm -rf vnc.cap')
    # json_data is default as None
    print result
    agent.post_report(subtask_id,
                      severity=0,
                      result=1,
                      brief='vnc',
                      detail=u'vnc',
                      json_data={'result': str(result)[100:15000]})

# Execute this while run this agent file directly
if not is_load_external():
    vnc(0, 0)
    # Run agent
#     agent.run()
    #os.system('bash spice/run.sh')
    
    
