#!/usr/bin/env python3
#coding: utf-8
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

sender = 'gzhxzb@qq.com'
receiver = ['55389758@qq.com','3232088054@qq.com']
subject = 'python email test'
smtpserver = 'smtp.qq.com'
username = 'gzhxzb'
password = 'abc957081'

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['From']=sender
#也可以编码
#msg['From']=sender.encode()
#显示友好名称
#msg['From']=_format_addr(u'Python爱好者 <%s>' % sender)
#msg['To']=_format_addr(receiver)
# msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
msg['Subject'] = "Link 中国 python"
# msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
#构造附件
att = MIMEText(open('D:\\Python27\\LICENSE.txt', 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="LICENSE.txt"'
msg.attach(att)

smtp = smtplib.SMTP()
smtp.connect(smtpserver)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()