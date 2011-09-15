# $Id: logger.py 1015 2010-12-03 21:13:28Z gwilladsen $

import smtplib
import time,datetime
import traceback
import pprint
import socket
from email.mime.text import MIMEText


class OutboundEmail(object):
        server = 'smtp-auth.no-ip.com'
        port = 25
        login = 'pygotham@thepeoplesconference.com'
        password= '4ed5rf6tg7yh'
        tls= True
        debug_level= 10
        from_addr= "pygotham@thepeoplesconference.com"
        to_addrs= 'pygotham@thepeoplesconference.com'

        def __init__(self):
                pass

        def send(self,to_addrs,subject,msg):
            server = smtplib.SMTP(self.server,self.port)
            server.set_debuglevel(self.debug_level)
            retry=3
            msg = MIMEText(msg,'html')
            msg['From'] = self.from_addr
            msg['To'] = ', '.join(to_addrs)
            msg['Subject'] = subject

            while retry > 0:
                try:
                    server.ehlo()
                    if self.tls:
                        server.starttls()
                        server.ehlo()
                    server.login(self.login,self.password)
                    server.sendmail(self.from_addr, to_addrs, msg.as_string())
                    retry=0
                    infostring =  " OutboundEmail:send(): Send succeeded, " + str(retry) + " retries left: msg:" + msg.as_string() + ", recipients:" + pprint.pformat(to_addrs)
                    print infostring
                except:
                    errstring =  " OutboundEmail:send(): Error: Send failed, RETRYING, " + str(retry) + " retries left: msg:" + msg.as_string() + ", recipients:" + pprint.pformat(to_addrs)  + " Traceback:" + traceback.format_exc()
                    print errstring
                    retry -= 1
                    time.sleep(5)
                try:
                    server.quit()
                except:
                    pass

if __name__ == "__main__":
    oe = OutboundEmail().send(["aagg@comcast.net","pygotham@thepeoplesconference.com"],"test 123", "test message")

