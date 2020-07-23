from datetime import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers, status
from rest_framework.response import Response
# from rest_framework.serializers import ModelSerializer

from course.models import Course, CourseExpire
from order.models import Order, OrderDetail


class GenerateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=('id','order_number','pay_type')

        extra_kwargs={
            'id':{'read_only':True},
            'order_number': {'read_only': True},
            'pay_type': {'write_only': True},
        }

    def validate(self, attrs):
        pay_type=attrs.get('pay_type')#对支付类型进行验证判断
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError('你的支付类型不在我们的服务范围内，很抱歉')
        return attrs
    def create(self, validated_data):#重写create方法生成订单
        redis_connection = get_redis_connection('shopping_cart')  # 连接redis数据库
        #self.context['request']获取request对象
        user_id=self.context['request'].user.id
        # user_id=22
        add=redis_connection.incr('order')
        #生成唯一订单号
        orderId=datetime.now().strftime('%Y%m%d%H%M%S')+'%06d'%user_id+'%06d'%add
        #生成订单
        order=Order.objects.create(
            order_title='购买课程记录信息',
            total_price=0,
            real_price=0,
            order_number=orderId,
            pay_type=validated_data.get('pay_type'),
            credit=0,
            order_desc='买到就是赚到',
            user_id=user_id,
        )
        #开启事务
        with transaction.atomic():
            rollback=transaction.savepoint()#如果以下内容出错则回到这个位置
            #获取购物车信息
            cart_list = redis_connection.hgetall('cart_%s' % user_id)
            status_list = redis_connection.smembers('status_%s' % user_id)
            for course_id_byte, expire_id_byte in cart_list.items():
                course_id = int(course_id_byte)
                expire_id = int(expire_id_byte)
                if course_id_byte in status_list:
                    try:
                        # 获取到的所有的课程信息
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        transaction.savepoint_rollback(rollback)#如果获取课程出错则数据回滚
                        raise serializers.ValidationError('商品不存在')

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
                    try:
                        # 生成订单详情
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=price,
                            real_price=mfg_true_price,
                            discount_name=course.activities_name
                        )
                    except:
                        transaction.savepoint_rollback(rollback)  # 如果生成订单出错则数据回滚
                        raise serializers.ValidationError('订单生成失败')
                    #计算订单总价
                    order.total_price+=float(price)
                    order.real_price+=float(mfg_true_price)

                    # 删除
                    redis_connection = get_redis_connection('shopping_cart')  # 连接redis数据库
                    redis_connection.hdel('cart_%s' % user_id,course.id)
                order.save()

            return order














































































































































