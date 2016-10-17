#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'"\"a\\\ne,\"r",dd,a' 对类似这种字符串进行分析的类,
最终生成一个['a\\\ne', 'r', 'dd', 'a']
'''

import sys

class ArrayLexer(object):
    def __init__(self):
        self._index = 0
        self._text = ""
        self._textList = []
        self._curValue = ""
        self._length = 0

    def prase(self, text):
        if (len(text) <= 0):
            raise Exception(u"文本长度为0")

        self._text = text
        self._length = len(text)

        # print (self._text)
        # print (self._length)
        #
        # print ('====================')

        while self._index < self._length:
            # ch = self.curChar()
            # print ('index == %d  || ch == %s' % (self._index, ch))
            out = ''
            while self._index < self._length and self.curChar() != ',':
                # print ('index == %d  || ch == %s' % (self._index, self.curChar()))
                if (self.curChar() == '"'):
                    self.nextIndex()
                    out = ''
                    while self.curChar() != '"':
                        if self.curChar() == '\\':
                            self.nextIndex()

                            if self.curChar() == 'r':
                                pass
                            elif self.curChar() == '"':
                                out += '\"'
                            elif self.curChar() == 'n':
                                out += '\n'
                            elif self.curChar() == 't':
                                out += '\t'
                            elif self.curChar() == '\\':
                                out += '\\'

                            self.nextIndex()
                        else:
                            out += self.curChar()
                            self.nextIndex()

                    # self._textList.append(out)
                    self.nextIndex()
                else:
                    # print ('out %s' % self.curChar())
                    if self.curChar() == '\\':
                        self.nextIndex()

                        if self.curChar() == 'r':
                            pass
                        elif self.curChar() == '"':
                            out += '\"'
                        elif self.curChar() == 'n':
                            out += '\n'
                        elif self.curChar() == 't':
                            out += '\t'
                        elif self.curChar() == '\\':
                            out += '\\'
                    else:
                        out += self.curChar()

                    self.nextIndex()

            self._textList.append(out)
            self.nextIndex()

        return  self._textList

        # print 'textList = ', self._textList

    def curChar(self):
        ch = self._text[self._index]
        return ch

    def nextIndex(self):
        self._index += 1
        # print('index: %d' % self._index)

    def getTextList(self):
        return self._textList

def test():
    if len(sys.argv) != 2:
        print 'Please specify one filename on the command line.'
        sys.exit(1)

    filename = sys.argv[1]
    body = file(filename, 'rt').read()
    print 'ORIGINAL:', repr(body)
    print '\n'
    # body = '"\\",4","5\\"6"'
    # print 'ORIGINAL:', repr(body)
    print '\n'

    lex = ArrayLexer()
    lex.prase(body)
    print(lex.getTextList())

if __name__ == '__main__':
    test()




