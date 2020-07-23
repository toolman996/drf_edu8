from drf_bzedu.settings import count
from my_celery.main import app
import logging

from drf_bzedu.utils.SMS import Sms

log=logging.getLogger('django')
# 储存任务的地方必须在tasks方法中
@app.task(name='send_message')
def send_message(mobile,code):
    message = Sms(count.API_KEY)
    status=message.send_message(mobile, code)

    if not status:
        log.error('短信发送失败，手机号为%s'%mobile)
    return 'success'




@app.task(name='send_emil')
def send_emil():
    print('发送邮件')

    return '成功'