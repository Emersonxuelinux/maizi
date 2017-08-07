'''
请写出最简单鸭子类型,并说说你对鸭子类型的理解?
我的理解：
在鸭子类型中，关注的不是对象的类型本身，而是它是如何使用的。
函数接受一个类型，本来它是想要接受鸭子类型，可是可能接受的不是一个鸭子类型，但是却可以表现出鸭子的动作和属性，那么这种情况下，我们称这个接受的类为鸭子类型。而如果接受的类型不能表现为鸭子的动作和属性，那么抛出错误即可。
'''
class duck:
    def gaga(self):
        print ('这是一只鸭子')
        
class bird:
    def gaga(self):
        print ('这是一只鸟')
class chick:
    def jiji(self):
        print ('这是一只鸡')

print (duck.gaga(duck()))
print (duck.gaga(bird()))
print (chick.gaga(chick()))
