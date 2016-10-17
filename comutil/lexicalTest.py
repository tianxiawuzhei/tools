#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''

import sys
# reload(sys)
# sys.setdefaultencoding('UTF-8')

import json
import arrayLexer
import codecs
import re
import utils

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
# body = '"\\\\4","5\\\\6"'
# print 'ORIGINAL:', repr(body)
# print '\n'
#
# lex = lexical.lexical()
# print (json.dumps(lex.prase(body), sort_keys=True, indent=2, ensure_ascii=False))
# #relutl:
# # ORIGINAL: '"\\\\4","5\\\\6"'
# #
# #
# # [
# #   "\\4",
# #   "5\\6"
# # ]
#
#
# #test3
# body = '"\\"a\\\\\ne,\\"r",d\n\\\\d,a'
# print 'ORIGINAL:', repr(body)
# print '\n'
#
# lex = lexical.lexical()
# print (json.dumps(lex.prase(body), sort_keys=True, indent=2, ensure_ascii=False))
# # relust
# # ORIGINAL: '"\\"a\\\\\ne,\\"r",dd,a'
# #
# #
# [
#   "\"a\\\ne,\"r",
#   "dd",
#   "a"
# ]

class dictlexer(object):
    def __init__(self):
        self._cursor = 0
        self._endCursor = 0
        self._text = ''
        self._dic = {}


    def parseText(self, text):
        if len(text) <= 0:
            print ("error: ", u'文本长度为0,不符合要求')

        # text = str(text)
        # self._text = str(text)
        self._text = text
        self._endCursor = len(text)
        return self._decodeComma(text)

    # k : v
    def _decodeKV(self, kvText):
        cursor = 0

        kvStr = kvText
        # kvStr = str(kvText)
        endCursor = len(kvStr)
        # print (kvStr)
        # print (endCursor)
        #key
        k = ''

        while kvStr[cursor] != ':' and cursor < endCursor:
            k += kvStr[cursor]
            # print (k)
            # print (cursor)
            cursor += 1

        if kvStr[cursor] != ':':
            raise Exception("key value not have : to separate")

        cursor += 1
        # out = self._praseStr(kvStr[cursor:])
        out = kvStr[cursor:]
        if utils.is_number(out):
            if '.' in out:
                self._dic[k] = float(out)
            else:
                self._dic[k] = int(out)
        else:
            self._dic[k] = out

    #解析逗号分割
    def _decodeComma(self, text):
        while True:
            if (self._cursor >= self._endCursor):
                break

            out = u''
            while self._cursor < self._endCursor and self._curChar() != ',':
                if self._curChar() == '"':
                    self._nextCursor()
                    while self._curChar() != '"':
                        if self._curChar() == '\\':
                            self._nextCursor()
                            if self._curChar() == 'r':
                                pass
                            elif self._curChar() == '"':
                                out += '\"'
                            elif self._curChar() == 'n':
                                out += '\n'
                            elif self._curChar() == 't':
                                out += '\t'
                            elif self._curChar() == '\\':
                                out += '\\'

                            self._nextCursor()
                        else:
                            out += self._curChar()
                            self._nextCursor()

                else:
                    out += self._curChar()

                self._nextCursor()

            # print repr(out)
            self._nextCursor()
            self._decodeKV(out)

        return self._dic

    def _curChar(self):
        if self._cursor < self._endCursor:
            return self._text[self._cursor]
        else:
            raise IndexError("text index out of range.", self._cursor, self._endCursor)


    def _nextCursor(self):
        self._cursor += 1

if __name__ == '__main__':
    # test1 文件方式
    if len(sys.argv) != 2:
        print 'Please specify one filename on the command line.'
        sys.exit(1)

    filename = sys.argv[1]
    fileObj = codecs.open(filename, "r", "utf_8")
    body = fileObj.read()
    print body
    # body = r'1:2.0,ne:"\\a\nc"'
    # print 'ORIGINAL:', body
    # print '\n'
    # #
    #
    #
    lex = dictlexer()
    print (json.dumps(lex.parseText(body), sort_keys=True, indent=2, ensure_ascii=False))









