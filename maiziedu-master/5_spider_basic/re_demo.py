# -*- coding: utf-8 -*-
'''
？
yes or not,放在后面表示可能有可能没有

^​
Matches the beginning of the line.
$ ​
Matches the end of the line. 

. ​
Matches any character (a wildcard). 

\s ​
Matches a whitespace character. 

\S ​
Matches a non-whitespace character (opposite of \s). 

* ​
Applies to the immediately preceding character and indicates to match zero or more of the preceding character. 

*? ​
Applies to the immediately preceding character and indicates to match zero or more of the preceding character in “non-greedy mode”. 

+ ​
Applies to the immediately preceding character and indicates to match zero or more of the preceding character. 

+? ​
Applies to the immediately preceding character and indicates to match zero or more of the preceding character in “non-greedy mode”. 

[aeiou] ​
Matches a single character as long as that character is in the specified set. In this example, it would match “a”, “e”, “i”, “o” or “u” but no other characters. 

[a-z0-9] ​
You can specify ranges of characters using the minus sign. This example is a single character that must be a lower case letter or a digit. 

[^A-Za-z] ​
When the first character in the set notation is a caret, it inverts the logic. This example matches a single character that is anything other than an upper or lower case character. 
( ) ​
When parentheses are added to a regular expression, they are ignored for the purpose of matching, but allow you to extract a particular subset of the matched string rather than the whole string when using findall(). 
\b ​
Matches the empty string, but only at the start or end of a word. 
\B ​
Matches the empty string, but not at the start or end of a word. 
\d ​
Matches any decimal digit; equivalent to the set [0-9]. 
\D ​
Matches any non-digit character; equivalent to the set [^0-9]
'''
import re


def re_demo():
    # 解析价格
    txt = 'If you purchase more than 100 sets, the price of product A is $9.90.'
    # 解析数量和价格: pattern/string/MatchObject
    m = re.search(r'(\d+).*\$(\d+\.?\d*)', txt)
    print(m.groups())

def re_method():
    # search vs. match
    # match从字符串开头开始匹配，search只要找到一个就可以了
    print(re.search('c', 'abcd'))
    print(re.match('c', 'abcd'))
    print(re.search('^c', 'abcd'))  # ^一定是从开头开始匹配，等同于match('c',abcd)
    print(re.match('.*c', 'abcd'))  # 等同于search('c',abcd)
    m = re.match('(.*)c', 'abcd')
    print(m.group(0), m.group(1))

    # split：使用正则表达式来分割，
    s1 = 'Hello, this is Joey'
    print(re.split(r'\W+', s1))  # \W指非字母，也就是说这里是把任意非字母符号作为分隔符

    # findall:返回所有匹配项
    s1 = 'Hello, this is Joey'
    s2 = 'The first price is $9.90 and the second price is $100'
    print(re.findall(r'\w+', s1))
    print(re.findall(r'\d+', s2))

    # findall vs. search
    print(re.search(r'\d+', s2).group())

    # finditer：返回迭代器，可以用循环处理
    s2 = 'The first price is $9.90 and the second price is $100'
    for m in re.finditer(r'\d+', s2):
        print(m.group())

    # sub ：返回替换的字符串
    s2 = 'The first price is $9.90 and the second price is $100'
    print(re.sub(r'\d+', '<number>', s2))
    # subn ：在sub的基础上多返回n，也就是替换了多少个
    print(re.subn(r'\d+', '<number>', s2))




def re_match_object():
    # group：用括号表示分组，这样会分别匹配并分组，可以用下标来指定
    s1 = 'Joey Huang'
    m = re.match(r'(\w+) (\w+)', s1)
    print(m.group(0, 1, 2))  # 0指代全部，1指代第一组，2指代第二组
    print(m.groups())  # 返回从1开始后面所有匹配组


def re_pattern_syntax():
    # dot：匹配任意项
    print(re.match(r'.*', 'abc\nedf').group())
    # 注意\n,如果没有DOTALL(),那么.不能指代\n,而\n是指换行，也就是说只会匹配到abc
    print(re.match(r'.*', 'abc\nedf', re.DOTALL).group())

    # caret：脱字号，指代开头，以之开头
    print(re.findall(r'^abc', 'abc\nabc'))
    # re.MULTILINE匹配多行，意思就是从\n之后又算作从开头匹配
    print(re.findall(r'^abc', 'abc\nabc', re.MULTILINE))

    # $：每行结尾，与脱字符配对记忆
    print(re.findall(r'abc.$', 'abc1\nabc2'))
    print(re.findall(r'abc.$', 'abc1\nabc2', re.MULTILINE))

    # *:0到多
    # +:1到多
    # ?:0或1
    print(re.match(r'ab*', 'a'))
    print(re.match(r'ab+', 'a'))
    print(re.match(r'ab?', 'a'))

    # greedy/non-greedy：查大还是查小
    s = '<H1>title</H1>'
    # 默认贪婪模式，这个会全部匹配<............>
    print(re.match(r'<.*>', s).group())
    # ?指非贪婪，也就是最短匹配
    print(re.match(r'<.*?>', s).group())

    # {m}：匹配m次
    print(re.match(r'ab{2}', 'abb').group())
    # {m,n}/{m,}：匹配m到n次/至少出现m次
    print(re.match(r'ab{2,4}', 'abbbbbb').group())
    print(re.match(r'ab{2,5}', 'ab'))
    print(re.match(r'ab{2,}', 'abbbbbb').group())
    # {m,n} non-greedy
    print(re.match(r'ab{2,4}?', 'abbbbbb').group())

    # 转义字符 \ 用来匹配特殊字符，有了r就是不需要再转义，少写\，体验更好
    print(re.search(r'\$(\d+\.\d+)', 'The price is $9.00').groups())

    # [] 集合:把匹配可能性写入
    print(re.search(r'0[xX]([0-9A-Fa-f]+)', 'The hex value is 0xFF03D6').groups())
    print(re.search(r'[0-9]{3}-[0-9]{4}-[0-9]{4}', 'The Phone Number is 138-2231-2398').group())
    print(re.search(r'[0-9\-]+', 'The Phone Number is 138-2231-2398').group())

    # | ： 或者
    print(re.search(r'([0-9]|-)+', 'The Phone Number is 138-2231-2398').group())


def re_pattern_syntax_meta_char():
    # \number：和第number个匹配组是一样的，重复出现
    print(re.search(r'(.+) \1', 'the the').group())
    print(re.search(r'[0-9]{3}(-[0-9]{4})\1', 'The Phone Number is 138-2231-2398'))
    print(re.search(r'[0-9]{3}(-[0-9]{4})\1', 'The Phone Number is 138-2231-2231').group())


    # \d\D：匹配数字\非数字
    print(re.search(r'\d{3}-\d{4}-\d{4}', 'The Phone Number is 138-2231-2398').group())
    # \b匹配单词开头和结尾，这里的意思就是手机号前后都没有其他内容
    print(re.search(r'\b(\d{3}-\d{4}-\d{4})\b', 'The Phone Number is 138-2231-2398').group())
    # \D:匹配非数字
    print(re.search(r'(\D+)\d{3}-\d{4}-\d{4}', 'The Phone Number is 138-2231-2398').groups())



def re_pattern_flags():
    # \s\S: \s匹配空格，\S匹配非空格，space
    # 制表符：[ \t\n\r\f\v] \f: 换页 \v: 垂直制表
    print(re.match(r'Name:\s+([a-zA-Z]+)', 'Name: \tJoey').groups())
    print(re.match(r'\S+:\s*(\S+)', 'Name: Joey').groups())

    # \w\W: [a-zA-Z0-9_]，匹配字符\非字符
    print(re.match(r'(\w+)(\W+)(\w+)', 'Name: Joey').groups())

    # re.I/re.IGNORECASE
    print(re.match(r'(name)\W+(\w+)', 'Name: Joey'))
    print(re.match(r'(name)\W+(\w+)', 'Name: Joey', re.IGNORECASE).groups())

    # re.VERBOSE
    a = re.compile(r"""
                   \d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""")
    b = re.compile(r"""
                   \d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.VERBOSE)
    c = re.compile(r"\d+\.\d*")
    print(a.search('20.5'))
    print(b.search('20.5').group())
    print(c.search('20.5').group())

if __name__ == '__main__':
    re_pattern_flags()
