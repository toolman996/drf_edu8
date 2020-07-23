import random
def get_random_name():
    xing='赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    ming='豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖兰明媚金娜龙美善'
    X=random.choice(xing)
    M="".join(random.choice(ming) for i in range(2))
    name=X+M
    # print(name)
    return name



