'''
利用tkinter的标准库完成一个打字游戏的项目，游戏开始，从窗口顶部下落多个不同的字符（背景自选一幅图片），当用户录入到某个字符时，其背景图片消失，改为红色并向上运动，直到出了窗口；而没能打到的字符会落入窗口底部停留。在窗口的右上角有一个计分板，每录入正确一个字符，计10分。当用户完成一个级别（1000个字符的80%）后，游戏自动升级到第二个级别，下落速度提高，每次出现字母增多。
'''
from tkinter import *
import random
import time
class Alphabet(object):
    '''
        把下落的字符设计成类，相关属性和操作都放在这里,由于大量生成实例，除了考虑列表，还可以考虑采用工厂模式
    '''
    #构造方法初始化位置属性，包含字符图片，初始位置
    def __init__(self,alphabet,width,speed):
        self.alphabet = alphabet
        self.bg_path = 'type_game_bg/%s.gif' % alphabet
        self.bg = PhotoImage(file=self.bg_path)
        self.x = random.randint(0,width-50)
        self.y = 0
        self.speed = speed
    #这个方法控制字符运动状态,类方法，里面用列表同时控制多个字母运动情况,每个类都有自己的速度，速度是稳定的。
    @staticmethod
    def motion(cv,width,height,speed):
        time.sleep(0.025)
        for falling in fallings:
            falling.y += falling.speed
            cv.create_image(falling.x,falling.y,image=falling.bg)
            cv.update()
            if falling.y+falling.speed >= height:
                missings.append(falling)
                fallings.remove(falling)
        for flowing in flowings:
            flowing.y += flowing.speed
            flowing.bg = PhotoImage(file='type_game_bg/balloon.gif')
            cv.create_image(flowing.x,flowing.y,image=flowing.bg)
            cv.update()
            if flowing.y <= 0 : flowings.remove(flowing)
        for missing in missings:
            cv.create_image(missing.x,height-25,image=missing.bg)
            cv.update()
    #监听按键
    @staticmethod
    def type_event(event):
        print (event.char)
        for falling in fallings:
            if event.char == falling.alphabet:
                falling.speed = -2
                flowings.append(falling)
                fallings.remove(falling)
    #定义这个方法通知计分板类
    def notify(self):
        pass
if __name__ == '__main__':
    root = Tk()
    wd = 800
    hg = 600
    max = 4
    speed = 4
    canvas = Canvas(root,width = wd,height=hg,bg='white')
    canvas.focus_set()
    canvas.bind('<Key>',Alphabet.type_event)
    canvas.pack()
    fallings = [] #正在下落的字母列表
    flowings = [] #被击中之后上升的字母列表
    missings = [] #没有击中之后停在最下方
    alphabets = ['a','b','c','d','e','f','g']
    while True:
        Alphabet.motion(canvas,wd,hg,speed)
       # canvas.update()
        while len(fallings) < max:
            select = alphabets[random.randint(0,len(alphabets)-1)] 
            fallings.append(Alphabet(select,wd,speed))
    root.mainloop()


