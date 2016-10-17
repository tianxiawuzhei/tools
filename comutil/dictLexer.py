#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
分析 ',' 分割键值对,':'分割键和值 的文本,如果是value值是字符串,支持转义字符,但是需要用双引号引起来
最终转化为python中的dict.
eg: r'1:2.0,ne:"\\a\nc"'
'''

import sys
import utils

class DictLexer(object):
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

        #因为有 '1e3' 这样的数字字符串, 而且is_number会判断为数字
        #这里不支持科学计数的数字,所以如果字符串有 'e', 则直接判定为字符串
        #不进行整形或浮点型判别
        if 'e' in out:
            self._dic[k] = out
        else:
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