'''
观察者模式
：定义了内部的对象之间是1：n的关系，当一个对象的状态发生了变化，与这个对象相关联的数据都会同时发生改变。

类似报纸订阅，当订阅报纸后，一有更新就会自动收到，除非退订；这里我们将出版者称为“主题”（Subject），订阅者成为“观察者”（Observer）。

而在生活当中，我们可以通过邮局订阅杂志或者报纸，出版社通过订阅信息主动向我们
邮寄订阅的杂志或者报纸，这就观察者模式在生活中的一个典型应用，用Python和面向对象实现这一个场景的代码。

'''
class Publisher:
    '''
    这是发布者类，所有它的订阅者放在一个列表中，然后主要有添加，删除，提醒观察者这三个方法
    '''
    def __init__(self):
        self.observers = []
    def add(self,observer):
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print ('添加失败：{}'.format(observer))
    def remove(self,observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('删除失败：{}'.format(observer))
    def notify(self):
        [observer.notify(self) for observer in self.observers]


