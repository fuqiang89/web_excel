import sys,os
import datetime
from smtplib import SMTP_SSL as SMTP       # (port 465, uses SSL)
#from smtplib import SMTP                 #  (port 25, no encryption)
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
reload(sys)
sys.setdefaultencoding('utf8')
filename=sys.argv[0][sys.argv[0].rfind(os.sep)+1:]

class Mail():
    def __init__(self):
        self.text_subtype = 'plain'
        self.html_subtype ='html'
        self.SMTPserver = 'smtp.qq.com'
        self.sender =     'xxxx.com'
        self.USERNAME = 'xxx@qq.com'
        self.PASSWORD = "xxx"
    def Sendmail(self,to_users=['xxx@qq.com'],picname=[],subject='',
                 subtoye='html',content='null',filename=''):
        to_users=to_users
        filename=filename
        subject=subject
        subtoye=subtoye
        content=content
        html = """\
            <html>
            <head></head>
        <body>
        <h1 align="center"><font size="5" face="arial" color="red">
        </font></h1>
        <p><b> %s</b></p>
        """
        picname=picname
        if picname:
            for img_name in picname:
                html = html + ('<img src="cid:%s"><br>' % img_name.replace('.',''))
        html = html + """<p><i>(from %s)</i></p>
                        <p><i>(time: %s)</i></p>
                        </body>
                          </html>
                    """
        html =  html % (content,filename,datetime.datetime.now())
        try:
            msg = MIMEMultipart()

            text = MIMEText(html,subtoye)
            msg.attach(text)
            if picname:
                for img in picname:
                    img_data = open(img, 'rb').read()
                    image = MIMEImage(img_data, name=os.path.basename(img))
                    image.add_header('Content-ID', '<%s>' % img.replace('.',''))
                    msg.attach(image)

            msg['Subject']= subject
            msg['From']   = self.sender # some SMTP servers will do this automatically, not all
            conn = SMTP(self.SMTPserver)
            conn.set_debuglevel(False)
            conn.login(self.USERNAME, self.PASSWORD)
            try:
                conn.sendmail(self.sender,to_users, msg.as_string())
                conn.close()
                return True
            except Exception,e:
                print(e)
                print(sys.exc_info())
                conn.close()
                return False
        except Exception, exc:
                print(e)
                print str(exc)
                return False
#                sys.exit( "mail failed; %s" % str(exc) )


sendmail=Mail()
if __name__ =='__main__':
    mail=Mail()
    bb=mail.Sendmail(to_users=['xxx@qq.com'])
    print(bb)
