import logging

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from course.models import Course, CourseExpire
from drf_bzedu.settings import count

log = logging.getLogger('django')


# 购物车的查询和添加处理
class ShoppingCartViewSet(ViewSet):
    # 登录成功才能访问接口
    permission_classes = [IsAuthenticated]

    # 添加购物车
    def add_shoppingcart(self, request):
        course_id = request.data.get('course_id')  # 课程id
        user_id = request.user.id  # 用户id
        my_status = True  # 勾选状态
        time = 0  # 有效期默认永久

        # 如果检验成功才能保存信息
        try:
            Course.objects.get(is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数传递错误，没有相关课程'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 获取redis数据库连接对象
            redis_connection = get_redis_connection('shopping_cart')
            pipeline = redis_connection.pipeline()  # 声明保存对象
            pipeline.multi()  # 开启管道
            pipeline.hset('cart_%s' % user_id, course_id, time)  # 将商品信息保存到集合中
            pipeline.sadd('status_%s' % user_id, course_id)  # 将勾选的商品保存到字典中
            pipeline.execute()  # 执行操作
            count = redis_connection.hlen('cart_%s' % user_id)  # 取数量
        except:
            log.error('购物车储存数据库失败')
            return Response({'message': '执行过程出错，购物车添加失败'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({'message': '添加购物车成功', 'course_count': count})

    # 查询购物车并展示
    def inquirt_cart(self, request):
        user_id = request.user.id
        # user_id = 22
        redis_connection = get_redis_connection('shopping_cart')
        cart_list_bytes = redis_connection.hgetall('cart_%s' % user_id)
        select_list_bytes = redis_connection.smembers('status_%s' % user_id)
        print(cart_list_bytes, select_list_bytes)
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                # 获取到的所有的课程信息
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue

            data.append({
                'selected': True if course_id_byte in select_list_bytes else False,
                "course_img": count.IMAGE_URL + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                # 'pirce': course.price,
                'mfg': course.mfg,
                'true_price': course.mfg_true_price(expire_id)
            })
        return Response(data)

    # 改变勾选状态
    def chanage_status(self, request):
        user_id = request.user.id
        select_status = request.data.get('selected')  # 获取单选框状态
        course_id = request.data.get('course_id')  # 课程id

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数传递错误，没有相关课程'}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection('shopping_cart')
        # 如果为真则添加
        if select_status:
            redis_connection.sadd('status_%s' % user_id, course_id)
        else:  # 否则删除
            redis_connection.srem('status_%s' % user_id, course_id)

        return Response({'message': 'success'}, status=status.HTTP_200_OK)

    # 删除逻辑
    def delect(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')  # 课程id
        try:  # 首先判断课程信息是否存在
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数传递错误，没有相关课程'}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection('shopping_cart')  # 连接redis数据库
        if course_id and course:
            redis_connection.hdel('cart_%s' % user_id, course_id)
        return Response({'message': '删除成功'}, status=status.HTTP_200_OK)

    def revise_mfg(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')  # 课程id
        mfg_id = request.data.get('mfg_id')  # 有效期id
        print(course_id, mfg_id)
        try:  # 首先判断课程信息是否存在
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            if mfg_id > 0:
                mfg = CourseExpire.objects.filter(is_show=True, is_delete=False, pk=mfg_id)
                if not mfg:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({'message': '参数传递错误，没有相关课程'}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection('shopping_cart')  # 连接redis数据库
        redis_connection.hset('cart_%s' % user_id, course_id, mfg_id)
        true_price = course.mfg_true_price(mfg_id)
        return Response({'message': '有效期切换成功', 'true_price': true_price}, status=status.HTTP_200_OK)

    # 获取购物车中勾选的课程
    def pitch_shoppingcart(self, request):
        user_id = request.user.id
        # user_id = 22
        print(user_id)
        redis_connection = get_redis_connection('shopping_cart')  # 连接redis数据库
        # 查询当前用户的所有购物车商品
        cart_list = redis_connection.hgetall('cart_%s' % user_id)
        status_list = redis_connection.smembers('status_%s' % user_id)
        count_num = 0
        data = []
        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            if course_id_byte in status_list:
                try:
                    # 获取到的所有的课程信息
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue
                # 如果有效期id大于零则需要计算价格
                price = course.price
                mfg_text = '永久有效'
                try:
                    if expire_id > 0:
                        course_mfg = CourseExpire.objects.get(id=expire_id)
                        price = course_mfg.price  # 拿到有效期的原价
                        mfg_text = course_mfg.expire_text
                except CourseExpire.DoesNotExist:
                    pass
                # 计算经过优惠的有效期的价格
                mfg_true_price = course.mfg_true_price(expire_id)

                data.append({
                    "course_img": count.IMAGE_URL + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_text": mfg_text,
                    'price': price,
                    'true_price': '%.2f' % float(mfg_true_price),
                    'active_name': course.activities_name
                })
                count_num += float(mfg_true_price)
        return Response({'data_list': data, 'total': count_num}, status=status.HTTP_200_OK)
