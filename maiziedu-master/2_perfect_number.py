'''
第二次作业：完数
写一个函数，该函数能判断传入的参数是否是一个完数，如果是完数则返回True，否则返回False
提示：完数就是一个数等于他的因子之和，如6=1+2+3; 那么这个数就是完数。
'''
def isPerfect(args):
    factors = [i for i in range(1,args) if args%i==0]
    print (factors)
    print ('the sum of factors of %d is %d' % (args,sum(factors)))
    if args == sum(factors):
       print ('%d is perfect number' % args)
    else: print ('%d is not perfect number' % args)
args = int(input('please enter an integer number:'))
isPerfect(args)
