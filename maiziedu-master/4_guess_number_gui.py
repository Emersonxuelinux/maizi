# -*- coding: utf-8 -*-
'''
1、计算机在所设定的范围内随机生成一个数，作为被猜数
2、每猜一个数，计算机首先判断在不在所设定的范围：如果不在，提示用户重新输入；如果在，提示用户新的数字范围
3、增加有趣的互动语句，请尽情发挥吧
'''
import random
from tkinter import *
import tkinter.simpledialog as dl
import tkinter.messagebox as mb
root = Tk()
w = Label(root,text = "猜数字")
w.pack()

mb.showinfo("Let's rock",'让我们开始猜数字吧！')
number  = random.randint(1, 100)
while True:
    guess = dl.askinteger("Number","What's your guess")
    if guess == number:
        mb.showinfo("提示", "恭喜你猜对了！")
        break
    elif guess < number:
        mb.showinfo("提示", "猜的数要大一点")
    elif guess > number:
        mb.showinfo("提示", "猜的数要小一点")
print ('Done!')
