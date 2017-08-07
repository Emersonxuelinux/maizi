# -*- encoding:utf-8 -*-
from threading import *
import time,datetime,string,random
import math
import itertools
import tkinter
import threading
# from PIL import ImageTk
class Image:		#抽象类 实例化里面的基础数据
    """
    要出现的字符与图片的抽象父类。
    """
    def __init__(self,cnvs,position):
        self.cnvs =cnvs			#画布
        self.position = position #位置
        self.id_pntr = None
        self.direction = 1  #字符运动方向（-1代表向上，1代表向下）
        self.step = 20      #每次移动坐标
        self.maxy = int(cnvs.cget('height')) - 50   #离窗口底部50时失效
        self.miny =10                               #向上运动至离窗口顶部为10时消失

    def delete(self):	#建立一个delete的方法
        if self.id_pntr:
            self.cnvs.delete(self.id_pntr)

    #修改字符运动方向
    def set_direction(self,direction):		#建立一个设置方向的方法
        if direction in [-1,1]:
            self.direction = direction

    #改变字符的位置
    def change_position(self):			 #建立一个移动位置的方法
        self.position = [self.position[0],self.position[1] + self.step * self.direction]

    def move(self):				#建立一个移动的方法
        self.change_position()	 #调用改变位置的方法
        self.delete()			#调用删除的方法
        self.draw()				#调用画的方法

    
    def is_die(self):			#建立一个字符是否有效的方法
        return self.position[1] >= self.maxy		#如果 位置大于等于maxy 就返回真

    #字符是否该消失
    def is_disappear(self):		#建立一个字符是否消失的方法
        return self.position[1] <= self.miny	#如果位置小于等于miny 就返回真


class StrikeChar(Image):		#建立一个类《点击字符》 ，继承于Image
    """要练习的字符"""
    def __init__(self,cnvs,position):		#构造方法
        super().__init__(cnvs,position)		#初始化父类的构造方法
        self.char = random.choice(string.ascii_letters)	# 用choice方法随机取出字母来赋给char
        

    #绘制字符
    def draw(self):		#建立一个 画的方法
        self.id_pntr = self.cnvs.create_text(self.position,text=self.char)  # 从画布上创建一个文本文字（位置，和字符）

class CharBg(Image):	 #建立一个字符背景类 ，继承Image类
    def __init__(self,cnvs,position):	 #构造方法
        super().__init__(cnvs,position)	 #初始化父类的构造方法
        self.fill = "pink"  #背景填充颜色

    #绘制字符背景
    def draw(self):		#建立一个画的方法
        self.position2 = [i+21 for i in self.position]	#把遍历position里面的值加21 赋给position2
		#用cnvs.create_oval的方法画一个圆
        self.id_pntr = self.cnvs.create_oval(self.position,self.position2,fill=self.fill)

    #字符失效时修改背景色
    def died(self):	#建立一个失效时候改变字符背景颜色的方法
        self.fill = "#FFF"	 #这里修改的是白色


class Aim:	#建立一个Aim类
    """要练习的字符和背景"""
    def __init__(self,cnvs,positionx):	#构造函数
        position = [positionx,50]
        self.cb = CharBg(cnvs,[i-10 for i in position])	# 实例化一个字符背景类（画布，遍历出来的position 减去10）赋给cb
        self.sc = StrikeChar(cnvs,position)	#实例化一个点击字符类（画布，位置）赋值给sc
        self.draw()	#调用了draw方法

    def draw(self):	#建立一个draw方法
        self.cb.draw()	#调用cb的draw方法 其实也就是CharBg.draw
        self.sc.draw()	#调用sc的draw方法 其实也就是StrikeChar.draw

    def delete(self):	#建立一个删除方法
        self.cb.delete()	#调用cb的删除方法
        self.sc.delete()	#调用sc的删除方法
	
    def move(self):		#建立一个移动方法
        self.cb.move()	#调用cb的移动方法
        self.sc.move()	#调用sc的移动方法

    def is_die(self):	 #建立一个判断是否失效的方法
        return self.sc.is_die()	# 调用sc的is_die()方法 并返回布尔

    def is_disappear(self):	 #建立一个判断是否消失的方法
        return self.sc.is_disappear()	# 调用sc的is_disappear()方法 并返回布尔

    def set_direction(self):	#建立一个设置方向的方法
        self.sc.set_direction(-1)	# 调用sc的set_direction()方法 并给出值-1 既向上
        self.cb.set_direction(-1)	# 调用sc的set_direction()方法 并给出值-1 既向上

    def died(self):	#建立一个失效的方法
        self.cb.died()	 # 调用cb的.died()方法 会造成字符背景变成白色

class ScoreBoard:	#建立一个积分板的类
    """记分板"""
    def __init__(self,cnvs):	 #构造函数
        self.level = 0  #级别
        self.score = 0  #得分
        self.cnvs = cnvs	#画布
        self.position = [self.get_posx(),20]	#位置
        self.level_id = None
        self.score_id = None
        # self.draw_info()
        # self.draw()

    def get_posx(self):
        w = int(self.cnvs.cget('width'))
        return w - 80

    def add_score(self,score=10):	#建立一个加分的方法 score参数默认10
        self.score += score			 #self.score=self.score+score
        return self.score			#返回新的score的值

    def add_level(self,level=1):	#建立一个加等级的方法
        self.level += level			#self.level = level+self.level
        return self.level			#返回新的level的值

    def draw(self):	#建立一个draw的方法
        self.delete()	 #调用删除方法
		#用cnvs.create_text创建文本位置参数[self.position[0]+30,self.position[1]]，文本参数str(self.level)在赋值给level_id
        self.level_id = self.cnvs.create_text([self.position[0]+30,self.position[1]],text=str(self.level))
		#用cnvs.create_text创建文本位置参数[self.position[0]+30,self.position[1]+20]，文本参数str(self.score)在赋值给score_id
        self.score_id = self.cnvs.create_text([self.position[0]+30,self.position[1]+20],text=str(self.score))
        self.cnvs.update()	#调用.cnvs.update()方法

    #输出提示信息
    def draw_info(self):	#定义一个draw_info方法
		#用cnvs.create_text创建文本，位置参数self.position，文本参数'level:'
        self.cnvs.create_text(self.position,text='level:')
		#用cnvs.create_text创建文本，位置参数[self.position[0],self.position[1]+20]，文本参数'score:'
        self.cnvs.create_text([self.position[0],self.position[1]+20],text='score:')

    def delete(self):	 #定义一个 delete方法
        if self.level_id:	#假如 level_id 有值
            self.cnvs.delete(self.level_id)	#就用cnvs.delete删除level_id 
        if self.score_id:	#假如 score_id 有值
            self.cnvs.delete(self.score_id)	#就用cnvs.delete删除score_id

    def clear_score(self):	#定义一个 清除分的方法
        self.score = 0	#把score赋值为零

class MyCavans:			#定义一个mycavans类

    def __init__(self,root):	#构造函数
        self.root = root
        self.button = MyButton(self.root,self)	#实例化一个MyButton的类
		#调用tkinter.Canvas建造个根窗体宽900 高600 背景颜色白色 赋给self.canvas
        self.canvas = tkinter.Canvas(self.root,width=900,height=600,bg='#FFF')
        # image = Image.open("img.jpg")
        # im = ImageTk.PhotoImage(image)
        #
        # canvas.create_image(300,50,image = im)
        self.init_canvas()	#调用init_canvas()
        self.score_board = ScoreBoard(self.canvas)	#实例化一个积分板的类 传参数self.canvas
        self.totals = (self.score_board.level + 1) * 10     # 出现字符的总数等于 (等级+1)*10
        self.gen_chars_num_time = self.totals // 2          #每次出现的字符个数
        self.sleep_time = 0.5 / (self.score_board.level + 1)  #对应某个级别字符出现速度
        self.positions = self.get_positions()
        self.canvas.focus_set()
        self.canvas.bind("<Key>",self.deal_evnt)            #绑定画布的键盘事件
        self.canvas.pack()

    def deal_evnt(self,vnt):	
        # print(vnt.char)
        for item in self.down_chars:	#遍历未录入字符集
            if item.sc.char.lower() == vnt.char.lower():	#假如 遍历出来的字符小写等于当前处理的字符
                self.down_chars.remove(item)        #已录入的字符从未录入的字符集删除
                self.up_chars.append(item)          #已录入的字符添加到向上的字符集
                item.set_direction()                #设定运动方向
                item.died()
                self.score_board.add_score()        #加分
                self.score_board.draw()             #显示分数
                break

    def init_canvas(self):
        self.down_chars = []                        #未录入字符集
        self.up_chars = []                          #已录入字符集
        self.die_chars = []                         #来不及录入的字符集
        self.fail_char = 0							#失败的字符
        self.canvas.delete("all")                   #清除画布

    def start(self):
        self.button.config(state="disabled")        #关闭开始按钮
        self.score_board.draw_info()                #显示记分器
        self.score_board.draw()						#把记分器从画布显示出来
        self.down_chars.append(Aim(self.canvas,random.choice(self.positions)))
        while self.down_chars or self.up_chars:     #进入练习循环  、当未录入和录入字符集里面有字符就循环
            for item in self.down_chars:            #处理未录入字符  遍历未处理的字符集
                if item.is_die():                      #如果字符没录入上
                    self.down_chars.remove(item)        #就从未录入的字符集 删除 这个字符
                    self.die_chars.append(item)         #就从没录入上的字符集加入这个字符
                    self.fail_char += 1                 #就 失败字符加1
                item.move()                         #否则就移动这个字符
            for item in self.up_chars:              #处理已录入字符 ，遍历 已经录入的字符集
                if item.is_disappear():             #假如 字符不存在
                    item.delete()                   #就删除这个字符
                    self.up_chars.remove(item)      #从已录入的字符集删除这个字符
                    self.fail_char += 1            #从失败的字符集加1
                else:
                    item.move()                     #否则就继续移动
            for item in self.die_chars:             #去除失效的字符，遍历 字符在来不及输入的字符集
                item.delete()                       #把遍历出来的字符删除
				#如果 所有字符集中的字符数量小于字符总数
            if self.fail_char + len(self.up_chars) + len(self.down_chars) + len(self.die_chars) < self.totals:
                current_positions = self.positions[:]
                for i in range(random.randint(0,self.gen_chars_num_time)): #产生新字符
                    position = random.choice(current_positions)	#用随机函数产生位置
                    current_positions.remove(position)	 #移除这个字符？？
                    self.down_chars.append(Aim(self.canvas,position))	#在未录入字符集添加字符 位置和 字符
            self.root.update()	 #调用update（）
            time.sleep(self.sleep_time)	#休眠时间 这里我设置初始0.5秒
        else:
            if self.score_board.score // 10 >= 0.8 * self.totals:
                self.score_board.add_level()        #命中率超过80%，升级
            self.score_board.clear_score()          #分数清空
            self.init_canvas()                      #初始化参数
            self.button.config(state='normal')      #启用开始按钮

    #计算字符可能出现的位置
    def get_positions(self):	#定义一个获得字符位置的方法
        w = int(self.canvas.cget('width'))	 # 估计就把画布的宽度传进去 ？
        char_width = 30	 #字符的宽度设置30
        positions = list(range(0,w,char_width))[1:w // char_width -1]
        positions = [i + char_width // 2 for i in positions]
        return positions

class MyButton:	#建立一个MyButton类
    """定制开始练习按钮"""
    def __init__(self,root,cvns):	#构造函数
        self.cvns = cvns	#画布参数
		#实例化一个按钮 （在根窗体中 ，文本是"来吧"，点击触发的时间是调用self.start）
        self.button = tkinter.Button(root,text = '来吧',command = self.start)
        self.button.pack()

    def start(self):  #开始的方法
        typing_start(self.cvns)

    def config(self,state):
        self.button.config(state=state)

#以线程的方式启动练习
def typing_start(cvns):
    t = threading.Thread(target=cvns.start)
    t.setDaemon(True)
    t.start()

if __name__ == '__main__':
    root = tkinter.Tk()
    cvns = MyCavans(root)
    typing_start(cvns)
    root.resizable(False, False)
    root.mainloop()
    print (active_count())
    print (threading.current_thread())
    print (enumerate())