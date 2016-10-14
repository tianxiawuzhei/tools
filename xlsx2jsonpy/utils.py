#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
一些常用工具方法
'''

#http://www.runoob.com/python3/python3-check-is-number.html
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


#不支持科学计数法
def is_float(s):
    if is_number(s) and '.' in s:
        return True
    else:
        return False

def test_is_number():
    print is_number(u'2.0')
    print is_number('2x.3')
    print(is_number(u'-foo'))  # False
    print(is_number(u'1'))  # True
    print(is_number(u'1.3'))  # True
    print(is_number(u'-1.37'))  # True
    print(is_number(u'1e3'))  # True

if __name__ == '__main__':
    pass
