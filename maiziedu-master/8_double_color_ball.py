'''
请使用面向对的方法,编写出双色球.要求:按照双色球开奖规则.将每次开奖的双色球保存到本地的txt文档里面,并双色球后面跟上日期.(提示,可能使用到库,random,time,os,sys等)
'''
import random
import time
ISOTIMEFORMAT='%Y-%m-%d %X'
class Ball():
    def get_nums(self,bottom,top,times):
        nums = [i for i in range(bottom,top+1)]
        poped = []
        for i in range(1,times+1):
            select = random.randint(1,len(nums))
            poped.append(nums.pop(select-1))
        return poped
    def get_simple(self):
        simple_red = self.get_nums(1,33,6)
        simple_blue = self.get_nums(1,16,1)
        with open('double_color_record.log','a') as f:
            now = time.strftime( ISOTIMEFORMAT,time.localtime() )
            f.write('------  --- %s \n' % now)
            f.write('红色球记录:\n')
            while simple_red : f.write('%d \n' % simple_red.pop())
            f.write('蓝色球记录:\n')
            while simple_blue : f.write('%d \n' % simple_blue.pop())
    def run(self):
        for i in range (1,100):
            self.get_simple()
if __name__=='__main__':
    b = Ball()
    b.run()
