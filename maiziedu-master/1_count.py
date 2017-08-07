# coding: UTF-8
'''
题目：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。
程序分析：isalpha方法判断是否是字母，isspace方法判断是否是空格，isdigit方法判断是否是数字
'''
#从版本3.0 开始去掉了raw_input 函数，改用input。所以两个函数合并在了一起
scen = input('Enter a scentence:')
alpha = space = digit = rest = 0
for s in scen:
    if str.isalpha(s):alpha +=1
    elif str.isspace(s):space +=1
    elif str.isdigit(s):digit +=1
    else: rest +=1

print('字母个数：'+str(alpha))
print('空格个数：'+str(space))
print('数字个数：'+str(digit))
print('其他个数：'+str(rest))
