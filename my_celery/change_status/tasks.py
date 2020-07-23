from my_celery.main import app

# 储存任务的地方必须在tasks方法中
@app.task(name='send_order')
def send_order():
    print('ok')

    return 'oky'