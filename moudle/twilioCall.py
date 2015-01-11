#coding=utf8
__author__ = 'fuqiang'
from urllib import urlencode
from twilio.rest import TwilioRestClient
from twilio import twiml

class TwilioCallNotifier():
    '''
    Twilio Call Notifier
    '''
    def __init__(self):
        self.voice='alice'
        self.language='zh-CN'
        self.loop=3
        self.token='672cce676d48607ce5cfb960378b1752'
        self.sid='ACbedcf286eec27acb8bc9ad81dbd32fd4'
        self.from_='+81345895170'
    def _mk_twiml(self, message):
        '''
        Make Twiml Say XML
        '''
        response = twiml.Response()
        response.addSay(message, voice=self.voice, language=self.language, loop=self.loop)
        return response.toxml()

    def notify(self, to, subject, message=None):
        '''
        Twilio Call notify
        '''
        token = self.token
        sid = self.sid
        from_ = self.from_
        if not to.startswith('+'):
            to = '+86' + to
        client = TwilioRestClient(sid, token)
        twiml_xml = self._mk_twiml(subject.decode('utf-8'))
        twiml_echo = urlencode({'Twiml': twiml_xml})
        twiml_url = 'http://twimlets.com/echo?' + twiml_echo
        method = 'POST'

        try:
            client.calls.create(
                url=twiml_url,
                method=method,
                from_=from_,
                to=to)
        except Exception, e:
            return False
        return True
CallMs=TwilioCallNotifier()
if __name__ == '__main__':
    call=TwilioCallNotifier()
    call.notify('8613799848615','你有一封端口扫描邮件，请查收！')
