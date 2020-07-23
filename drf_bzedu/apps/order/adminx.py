import xadmin

from order.models import Order, OrderDetail


class orderModelAdmin(object):
    pass
xadmin.site.register(Order,orderModelAdmin)

class orderDetailModelAdmin(object):
    pass
xadmin.site.register(OrderDetail,orderDetailModelAdmin)














