#coding: utf-8

import os,re
#将a文件的字符去出在b文件中执行查找操作。如果存在就直接写入文件
def getselect(str):
    ftest=open('./v_id2','r')
    text=ftest.read()
    ftest.close()
    pos=text.find(str)
    if pos!=-1:
        print('查找成功')
        print str
        textfile=open('./v_final','a')
        textfile.write(str)
        #textfile.write('\n');
        textfile.close()
	
#取出a文件并直接调用
path=os.getcwd()
print path
myfile=file('./v_id1','r')
#每次读取一行保存到s中；
#进行判断
if(os.path.exists("./v_final")):
    open('./v_final','a').truncate(0)
else:
    os.system("touch ./v_final")
for s in myfile.readlines():
    getselect(s)
