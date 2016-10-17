# -*- coding: utf-8 -*-

import re
import utils

class ToLua:
    def __init__(self):
        self.depth = 0

        self.newline = '\n'
        self.tab = '\t'

    def encode(self, obj):
        if not obj:
            return
        self.depth = 0
        return self.__encode(obj)

    def __encode(self, obj):
        s = ''
        tab = self.tab
        newline = self.newline
        tp = type(obj)
        if obj == None:
            s += 'nil'
        elif tp in [str, unicode]:
            #处理转义字符
            obj = obj.replace('\\', r'\\')
            obj = obj.replace('\"', r'\"')
            obj = obj.replace('\n', r'\n')
            obj = obj.replace('\t', r'\t')
            obj = obj.replace('\r', r'')

            s += ("'" + obj + "'")
        elif tp in [int, float, long, complex]:
            s += str(obj)
        elif tp is bool:
            s += str(obj).lower()
        elif tp in [dict]:
            self.depth += 1
            if len(obj) == 0:
                newline = tab = ''
            dp = tab * self.depth
            s += "%s{%s" % (tab * (self.depth - 2), newline)

            ls = []
            for k, v in obj.iteritems():
                if utils.is_number(k):
                    item = dp + '[%s] = %s' % (k, self.__encode(v))
                else:
                    item = dp + '%s = %s' % (k, self.__encode(v))

                ls.append(item)

            s += (',%s' % newline).join(ls)

            self.depth -= 1
            s += "%s%s}" % (newline, tab * self.depth)
        elif tp in [list, tuple]:
            self.depth += 1
            if len(obj) == 0 or len(filter(lambda x:  type(x) in (int,  float,  long) or (type(x) in [str, unicode] and len(x) < 10),  obj)) == len(obj):
                newline = tab = ''
            dp = tab * self.depth
            s += "%s{%s" % (tab * (self.depth - 2), newline)

            ls = []
            for v in obj:
                item = dp + self.__encode(v)
                ls.append(item)

            s += (',%s' % newline).join(ls)

            self.depth -= 1
            s += "%s%s}" % (newline, tab * self.depth)
        return s
