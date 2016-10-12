#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
用于测试shlex模块分割字符功能
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import lexical

#test1 文件方式
# if len(sys.argv) != 2:
#     print 'Please specify one filename on the command line.'
#     sys.exit(1)
#
# filename = sys.argv[1]
# body = file(filename, 'rt').read()
# print 'ORIGINAL:', repr(body)
# print '\n'

#test2 字符串方式
body = '"\\\\4","5\\\\6"'
print 'ORIGINAL:', repr(body)
print '\n'

lex = lexical.lexical()
print (json.dumps(lex.prase(body), sort_keys=True, indent=2, ensure_ascii=False))
#relutl:
# ORIGINAL: '"\\\\4","5\\\\6"'
#
#
# [
#   "\\4",
#   "5\\6"
# ]


#test3
body = '"\\"a\\\\\ne,\\"r",d\n\\\\d,a'
print 'ORIGINAL:', repr(body)
print '\n'

lex = lexical.lexical()
print (json.dumps(lex.prase(body), sort_keys=True, indent=2, ensure_ascii=False))
# relust
# ORIGINAL: '"\\"a\\\\\ne,\\"r",dd,a'
#
#
# [
#   "\"a\\\ne,\"r",
#   "dd",
#   "a"
# ]




