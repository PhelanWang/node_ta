# -*- coding:utf-8 -*-
#import logging
#from subprocess import *
#from commands import *
import time

import  os
#import sys
import re
#import random
import commands


mpath = ''
ndebug=True
# default bin  path  is '/usr/libexec' ,  bin name can set
# default module path is /usr/lib/..
class VnicTest(object):
    qemu_kvm = ''
    ttype = ''
    def __init__(self,binname,ttype):
        self.qemu_kvm = binname;
        self.ttype=ttype

    #only check if vms run
    def is_ready(self):
        pids= os.popen("pidof "+self.qemu_kvm+"").read().strip('\n').strip(' ');
        print pids
        if pids=='':
            return 'ok'
        else :
            return 'false'

    #if vms stop ,
    #   delete log begore test and
    #   begin replace bins and modules
    def begin(self):
        ready=self.is_ready();
        print "ready = "+ready
        if ready == "ok":
            os.system('rmmod vhost_net')
            is_file = os.popen("ls /var/log/ | grep 'vhost_pck.log'").read().strip("\n").strip(" ");
            if is_file =='vhost_pck.log':
                print "rm this file"
                os.system("rm  -f  /var/log/vhost_pck.log")
            ########################################################################
            if(ndebug==True):
                self.replace()
            os.system("rmmod vhost_net")
            print time.time()
#             time.sleep(60*5)
            print time.time()
            return True
        else:
            print "Stop all vms on this node!"
            return  False

    #if install replace bins and modules don need this function
    # replace qemu-kvm or vhost_net.ko
    def replace(self):
        if self.ttype == 'vhost':
            path = self.getpath()
            str = 'rm -f '+path+'vhost_net.ko'
            print str
            os.system(str)
            #os.system('mv '+path+'vhost_net.ko '+path+'vhost_net.bk')
            #os.system('mv '+path+'vhost.ko '+path+'vhost.bk')

            #currentpwd = commands.getstatusoutput('pwd');
            #curpath =  currentpwd[1]
            #str = 'cp '+curpath+'/vnic/vhost_net.ko '+path+''
            #print str
            str = 'cp '+path+'hacker/vhost_net.ko ' +path + ''
            print str
            os.system(str)
            #str = 'cp '+curpath+'/vnic/vhost.ko '+path+''
            #os.system(str)
            #print str


        if self.ttype == 'virtio':
            os.system('mv /usr/libexec/'+self.qemu_kvm+' /usr/libexec'+self.qemu_kvm+'.bk')
            os.system('cp ./qemu-kvm /usr/libexec/'+self.qemu_kvm+'')
            # cp default overwrite

    # This function need  all vms on this node had stopped ,
    # restore  the previous version
    def disreplace(self):
        flag = self.is_ready()
        while(flag!='ok'):
            self.shutdown()
            flag = self.is_ready()
        if flag == 'ok':
            if self.ttype == 'vhost':
                os.system("rmmod vhost_net")
                path = self.getpath()
                str = 'rm -f '+path+'vhost_net.ko'
                print str
                os.system(str)
                str = 'cp  '+path+'old/vhost_net.ko '+path+''
                print str
                os.system(str)
            if self.ttype == 'virtio':
                os.system('rm -f /usr/libexec/'+self.qemu_kvm+'')
                os.system('mv /usr/libexec/'+self.qemu_kvm+'.bk  /usr/libexec'+self.qemu_kvm+'')
                #os.system('cp ./qemu-kvm /usr/libexec/'+self.qemu_kvm+'')
        else :
            print "Stop all vms on this node !"

    def deal_hexdump(self):
#         os.popen('touch /var/log/vhost_pck.log')
        is_file = os.popen("ls /var/log/ | grep 'vhost_pck.log'").read().strip("\n").strip(" ");
        if is_file =='vhost_pck.log': 
             
#             os.system('text2pcap /var/log/vhost_pck.log  /var/log/vniclog')
#             out = commands.getstatusoutput("tshark -a duration:120 -Y 'http contains \"text/html\" and http contains \"HTTP/1.1 200 OK\"' -r /var/log/vniclog  -V")
#             str = out[1]
#             smpout = commands.getstatusoutput("tshark -a duration:120 -Y 'http contains \"text/html\" ' -r /var/log/vniclog ")
#             str2 = smpout[1]
            file = open("/var/log/vhost_pck.log", "r")
            str = file.read()
            
            htmlstr = re.findall(r'<html>.+?</html>', str, re.S)
#             htmlstr = re.findall(r'baidu.com', str, re.S)
            
            
            
            if (len (htmlstr) >=1):
                report = {
                    "brief": str,
                    "detail": htmlstr
                             }
            else :
                report={
                "brief":'未能旁路网卡数据',
                "detail":'请检查网络设置，正确访问网络并运行虚拟机'
                            }
    
        else :
            report={
                "brief":'未能旁路网卡数据',
                "detail":'请检查网络设置，正确访问网络并运行虚拟机'
                        }
        #print report["brief"]
        return report
        #for str1 in htmlstr:
            #print str1.decode('gbk').encode('utf-8')

    def shutdown(self):
         flag = self.is_ready()
         while(flag!='ok') :
             pids= os.popen("pidof "+self.qemu_kvm+"").read().strip('\n').strip(' ').split(' ')
             for pid in pids:
                 os.system("kill -9 "+pid)
             flag=self.is_ready()

    #return report and dis replace
    def stop(self):
        self.shutdown()
        #########################################
        if(ndebug==True):
            self.disreplace()
        return self.deal_hexdump()
        #self.getreport()

    # return  report
    def getreport(self):
        pass
    def getpath(self):
         #replace_reg = re.compile(r'vhost_net.ko$')
         #pwd = os.popen("find /lib/modules -name 'vhost_net\.ko' |grep $(uname -r)").read().strip('\n')
         #if(pwd==''):
         #    pwd = os.popen("find /usr/lib/modules -name 'vhost_net\.ko' |grep $(uname -r)").read().strip('\n')
         #path =  replace_reg.sub('',pwd)
         #print path +'path'
        return   '/usr/lib/modules/$(uname -r)/kernel/drivers/vhost/'
if __name__ == "__main__":
    vc  = VnicTest('qemu-kvm','vhost');
    #vc.begin()
    #vc.stop()
    report = vc.deal_hexdump()
    print report['brief']
    print report['detail']
    
    #time.sleep(10)
    #print '123'
