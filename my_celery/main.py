#主程序
import os

import django
from celery import Celery

#创建celery实例对象
app=Celery('edu')

# 把celery和django进行结合，识别并加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_bzedu.settings.develop')
django.setup()

#通过实例对象app调用加载配置
app.config_from_object('my_celery.config')

# 将添加任务到实例对象中  自动找到该目录下的tasks文件中的任务
# app.autodiscover_tasks(['任务1'，'任务2'])
app.autodiscover_tasks(['my_celery.send_message','my_celery.cp','my_celery.change_status'])

# 启动celery  在项目的跟目录下执行启动命令
# celery -A my_celery.main worker --loglevel=info