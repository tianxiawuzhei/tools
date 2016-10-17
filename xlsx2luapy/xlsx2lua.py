#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
将xls中第一个表转成json的工具
'''

import sys

import getopt, xlrd, os, os.path, json
import codecs

sys.path.append('..')
from comutil import Sheet

def errorHelp():
    print(u"发生了一些错误,请输入python xlsx2lua.py -h来获取帮助")

def showHelp():
    print u"""
-h 帮助
-i xlsx所在目录,必填
-o lua的输出目录,必填
例如:
python xlsx2lua.py -i 配置目录 -o 输出目录
"""

def xls2lua(xlsPath, xlsName):
    try:
        xlsfile = xlrd.open_workbook(xlsPath)
    except Exception, e:
        print("[ERROR] => get configuration file from %s faild!" % xlsPath)
        raise e

    # 根据索引来获取sheet
    mysheet = xlsfile.sheet_by_index(0)
    shet = Sheet.openSheet(mysheet)

    #保存到文件中
    try:
        f = codecs.open("%s/map_%s.lua" % (luaDir, xlsName.decode('utf-8')), 'w', 'utf-8')
        f.write(shet.toLua())
        print("INFO :" + xlsName.decode('utf-8') + "   " + u"转换成功")
    except Exception, e:
        print("ERROR :" + xlsName.decode('utf-8') + "   " + u"转换失败", e)
    finally:
        if f:
            f.close()

def toLua(xlsDir):
    for parent, dirnames, filenames in os.walk(xlsDir):
        for filename in filenames:
            # if filename in xlsList:
                if not filename.startswith("~"):
                    extension = os.path.splitext(filename)[1]
                    if (extension == ".xls" or extension == ".xlsx"):
                        xls2lua(os.path.join(parent, filename), os.path.splitext(filename)[0])


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])
        for option, value in opts:
            if option in ["-h","--help"]:
                showHelp()
                return
            elif option in ["-i", "--input"]:
                xlsDir = value
            elif option in ["-o", "--output"]:
                global luaDir
                luaDir = value
                if not os.path.exists(luaDir):
                    os.mkdir(luaDir)
        if not luaDir:
            luaDir = ''
        if not xlsDir:
            errorHelp()
        else:
            toLua(xlsDir)
    except getopt.GetoptError:
        errorHelp()

if __name__ == '__main__':
    main()