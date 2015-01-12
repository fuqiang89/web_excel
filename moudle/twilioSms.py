#coding=utf8
__author__ = 'fuqiang'
import sys
from urllib import urlencode
from twilio.rest import TwilioRestClient
from twilio import twiml

class TwilioSmsNotifier():
    '''
    Twilio Call Notifier
    '''
    def __init__(self):
        self.voice='alice'
        self.language='zh-CN'
        self.loop=3
        self.token='xxx'
        self.sid='xx'
        self.from_='xx'
    def sms(self,to,mes):
        if not to.startswith('+'):
            to = '+86' + to
        client = TwilioRestClient(self.sid, self.token)
        try:
            message = client.messages.create(body="{0}".format(mes),
                to=to,
                from_=self.from_)
            return True
        except Exception,e:
            print(sys.exc_info())
            print(e)
            return False
SMS=TwilioSmsNotifier()

if __name__ == '__main__':
    SMS.sms('xxx','测试 ')
