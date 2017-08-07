import re

if __name__ == '__main__':
    #1.判断字符串是否全部是小写字母
    str1 = 'dklinegl'
    '''
    还可以用re.search()和先编译成正则对象regex = re.compile('[a-z]+$')
,这样的好处是一处地方用正则表达式就行了，需要修改也只修改一处    
    '''
    an = re.match('[a-z]+$',str1)
    if an:
        print ('全是小写')
    else:
        print ('不全是小写')
    # 提取分组的字符串,数字：[0-9]+,字母:[a-z]+
    str2 = '780934lkngskgnh89'
    obj = re.search('([0-9]+)([a-z]+)([0-9]+)([a-z]+)',str2)
    print (obj.group(1))
    #从字符串中提取邮箱和手机号
    str3 = 'kling;eipqoieng13908219764l;oin3123'
    regex_phone = re.compile('((?:(?:13[0-9])|(?:15[^4,\D])|(?:18[0,2,5-9]))\d{8}')
    print (regex_phone.findall(str1))
