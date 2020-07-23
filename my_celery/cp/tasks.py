from my_celery.main import app

# 储存任务的地方必须在tasks方法中
@app.task(name='send_file')
def send_file():
    print('ok')

    return 'oky'