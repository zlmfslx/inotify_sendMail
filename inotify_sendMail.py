#coding=utf-8
# @Time    : 2018/5/22 15:19
# @Author  : zlmfslx
# @Oath    : Your happiness is my greatest satisfaction
# @File    : inotify_sendMail.py

import os
import smtplib
from email.mime.text import MIMEText
from pyinotify import WatchManager, Notifier, \
ProcessEvent,IN_DELETE, IN_CREATE,IN_MODIFY


class EventHandler(ProcessEvent):
 arr =['10634780@qq.com','tengxun@qq.com']
 """事件处理"""
 def process_IN_CREATE(self, event):
   dirName =event.path.split('/')[-1]
   name = event.name.split('.')[0]
   url = 'http://wiki.xiaoh.org/?file='+dirName+'/'+name
   print  "Create file: %s " %  os.path.join(event.path,event.name)
   self.send_mail(self.arr, '技术知识更新', event.name+'更新，求阅读,链接地址:'+url)
  #print event.path

 def process_IN_DELETE(self, event):
  #print  "Delete file: %s " %  os.path.join(event.path,event.name)
     self.send_mail(self.arr, '技术知识更新', event.name+'已经删除')

 def process_IN_MODIFY(self, event):
   dirName =event.path.split('/')[-1]
   name = event.name.split('.')[0]
   url = 'http://wiki.xiaoh.org/?file='+dirName+'/'+name
   #print  "Modify file: %s " %  os.path.join(event.path,event.name)
   self.send_mail(self.arr, '技术知识更新', event.name+'更新，求阅读,链接地址:'+url)
   #print event.name
 def send_mail(self,to_list,subject,content):
    #print 'hello 啊'
    mail_host = 'smtp.ym.163.com' #发件服务器地址  默认 163的
    mail_user = '' #邮箱
    mail_pass = ''#密码
    mail_postfix = ''#后缀
    me = "wiki知识共享中心"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = ','.join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        print str(e)
        return False

def FSMonitor(path='.'):
  wm = WatchManager()
  mask = IN_DELETE | IN_CREATE |IN_MODIFY
  notifier = Notifier(wm, EventHandler())
  wm.add_watch(path, mask,auto_add=True,rec=True)
  print 'now starting monitor %s'%(path)
  while True:
   try:
     notifier.process_events()
     if notifier.check_events():
       notifier.read_events()
   except KeyboardInterrupt:
     notifier.stop()
     break

if __name__ == "__main__":
 FSMonitor('/home/')

