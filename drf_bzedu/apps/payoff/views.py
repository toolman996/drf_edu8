import os
import logging
from datetime import datetime

from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay import AliPay

from course.models import CourseExpire
from drf_bzedu.settings.develop import BASE_DIR
from order.models import Order
from user.models import UserCourse


log=logging.getLogger()


# 支付宝支付开发
class PayOffAPIView(APIView):
    def get(self, request,*args,**kwargs):

        # 订单编号
        orderid = request.query_params.get("orderid")
        # orderid = 20200719231114000022000021

        # 公钥私钥
        private_key = open(os.path.join(BASE_DIR, "apps/payoff/keys/app_private_key.pem")).read()
        public_key = open(os.path.join(BASE_DIR, "apps/payoff/keys/alipay_public_key.pem")).read()

        # 查询订单如果，没有查询到订单直接return错误信息
        try:
            order = Order.objects.get(order_number=orderid)
        except Order.DoesNotExist:
            return Response({"message": '没有查询到相关的订单信息'}, status=status.HTTP_400_BAD_REQUEST)

        # 支付宝的初始化配置
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],  # 沙箱支付的id
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=private_key,#私钥
            alipay_public_key_string=public_key,#公钥
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"],
        )

        # 生成支付链接
        payoff_url = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,#订单号
            total_amount=float(order.real_price),# 总价格
            subject=order.order_title,# 商品的名字
            return_url=settings.ALIAPY_CONFIG["return_url"],
            notify_url=settings.ALIAPY_CONFIG["notify_url"]
        )

        # 生成好的地址包括两部分需要拼接
        url = settings.ALIAPY_CONFIG["gateway_url"] + payoff_url

        return Response(url)




# 支付成功后页面信息显示
class PayOffSuccessAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 公钥私钥
        private_key = open(os.path.join(BASE_DIR, "apps/payoff/keys/app_private_key.pem")).read()
        public_key = open(os.path.join(BASE_DIR, "apps/payoff/keys/alipay_public_key.pem")).read()

        # 支付宝的初始化配置
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],  # 沙箱支付的id
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=private_key,  # 私钥
            alipay_public_key_string=public_key,  # 公钥
            sign_type=settings.ALIAPY_CONFIG["sign_type"],
            debug=settings.ALIAPY_CONFIG["debug"],
        )

        #全路劲的url拼接接受全路径下的数据
        data=request.query_params.dict()
        sign=data.pop('sign')
        #
        # success=alipay.verify(data,sign)
        success=True
        if success:
            return self.order_result_show(data)
        return Response({'message':'支付失败'},status=status.HTTP_400_BAD_REQUEST)

    def order_result_show(self, data):

        # 先查询订单是否成功如果没有成功返回错误信息
        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number, order_status=0)
        except Order.DoesNotExist:
            return Response({"message": '支付失败,订单不存在'}, status=status.HTTP_400_BAD_REQUEST)
        #开启事务
        with transaction.atomic():
            point = transaction.savepoint()

            # 如果课程存在则说明支付成功修改订单数据
            try:
                order.pay_time = datetime.now()
                order.order_status = 1
                order.save()

                user = order.user
                order_detail_list = order.order_courses.all()# 获取订单中的所有课程
                course_list = []#需要展示的信息

                for result in order_detail_list:#遍历所有信息并保存修改
                    course = result.course
                    course.students += 1
                    course.save()

                    time = order.pay_time.timestamp()

                    # 如果有效期不是永久计算其价格是多少
                    if result.expire > 0:
                        expire = CourseExpire.objects.get(pk=result.expire)
                        expire_timestamp = expire.expire_time * 24 * 60 * 60
                        end_time = datetime.fromtimestamp(time + expire_timestamp)
                    else:
                        end_time = None

                    # 生成课程的信息
                    UserCourse.objects.create(
                        user_id=user.id,
                        course_id=course.id,
                        trade_no=data.get("trade_no"),
                        buy_type=1,
                        pay_time=order.pay_time,
                        out_time=end_time,
                    )

                    course_list.append({
                        "id": course.id,
                        "name": course.name
                    })

            except:
                log.error("数据有误请重试，请重试")
                transaction.savepoint_rollback(point)
                return Response({"message": '订单信息更新失败，请重试'}, status=status.HTTP_400_BAD_REQUEST)

        # 返回前端需要的数据
        return Response({"message": "支付成功",
                         "success": "success",
                         "pay_time": order.pay_time,
                         "real_price": order.real_price,
                         "course_list": course_list
                         },status=status.HTTP_200_OK)


















    # def order_result_show(self,data):
    #     orderid=data.get('out_trade_no')
    #     try:
    #         order=Order.objects.get(order_number=orderid)
    #     except Order.DoesNotExist:
    #         return Response({'message': '支付失败,订单不存在'}, status=status.HTTP_400_BAD_REQUEST)
    #     #开启事务
    #     with transaction.atomic():
    #         point=transaction.savepoint()
    #         # 如果课程存在则说明支付成功修改订单数据
    #         try:
    #             order.pay_time=datetime.now()
    #             order.order_status=1
    #             order.save()
    #
    #             user=order.user
    #             all_course=order.order_courses.all()#获取所有课程
    #
    #             course_data=[]
    #
    #             for result in all_course:
    #                 course=result.course
    #                 course.students+=1
    #                 course.save()
    #
    #             time=order.pay_time.timestamp()
    #             #更新有效期时间
    #             if result.expire>0:
    #                 expire=CourseExpire.objects.get(id=result.expire)
    #                 expire_out=expire.expire_time=24*60*60
    #                 end_time = datetime.fromtimestamp(time + expire_out)
    #             else:
    #                 end_time=None
    #             # 生成购买课程信息
    #             UserCourse.objects.create(
    #                 user_id=user.id,
    #                 course_id=course.id,
    #                 trade_no=data.get('trade_no'),
    #                 buy_type=1,
    #                 pay_time=order.pay_time,
    #                 out_time=end_time
    #             )
    #
    #             course_data.append({
    #                 "id":course.id,
    #                 'name':course.nme
    #             })
    #
    #         except:
    #             log.error('数据有误请重试')
    #             transaction.savepoint_rollback(point)
    #             return Response({'message': '订单信息更新失败，请重试'}, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({'message': '支付成功',
    #                      'success':'success',
    #                      'pay_time':order.pay_time,
    #                      'real_price':order.real_price,
    #                      'course_list':course_data}, status=status.HTTP_400_BAD_REQUEST)







