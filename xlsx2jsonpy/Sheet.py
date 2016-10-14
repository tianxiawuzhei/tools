#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import json
import math
import arrayLexer
import dictLexer
import types
from types import *
from xlrd import XL_CELL_EMPTY, XL_CELL_TEXT, XL_CELL_NUMBER, XL_CELL_DATE, XL_CELL_BOOLEAN, XL_CELL_ERROR, \
    XL_CELL_BLANK

class Field(object):
    def __init__(self):
        #配置字段名
        self.cfgName = None
        #中文字段名
        self.chinaName = None
        #字段类型
        self.type = None
        #使用类型
        self.userType = None

    def __str__(self):
        return "name:%r,type:%r" % (self.cfgName, self.type)

class Sheet(object):
    def __init__(self, shet):
        self.shet = shet
        self.name = shet.name

        #字段属性列表
        self.fieldList = []

        #解析的数据
        self.python_obj = {}

        self.__findRow()
        self.__findCol()

        self.__parseField()

        self.__convertPython()


    #查找数据起始行数，中文名称，配置名称，类型行，数据终止行数
    def __findRow(self):
        self.cfgNameRow = 0
        self.userRow = 1
        self.typeRow = 2
        self.chinaNameRow = 3
        self.dataStartRow = 4

        for row in range(self.shet.nrows):
            if self.shet.cell(row, 0).ctype == XL_CELL_EMPTY:
                self.dataEndRow = row
                break

        if row == self.shet.nrows - 1:
            self.dataEndRow = self.shet.nrows

    #查找数据终止列数
    def __findCol(self):
        #遍历查找，如果在excel中存在多余的注释，列数为第一个空字符串出现的单元格下标#
        for col in range(self.shet.ncols):
            if self.shet.cell(self.cfgNameRow, col).ctype == XL_CELL_EMPTY:
                self.dataEndCol = col
                break

        #若col未定义，则表示在excel中不存在多余的注释，则列数为整个表的列数#
        if col == self.shet.ncols - 1:
            self.dataEndCol = self.shet.ncols


    #解析字段属性
    def __parseField(self):
        for col in range(self.dataEndCol):
            field = Field()
            self.fieldList.append(field)

            #字段类型
            field.type = self.shet.cell(self.typeRow, col).value

            #字段名字
            field.cfgName = self.shet.cell(self.cfgNameRow, col).value

            field.chinaName = self.shet.cell(self.chinaNameRow, col).value

            field.userType = self.shet.cell(self.userRow, col).value

    #转换字符串为list
    def __convertStrToList(self, strx, typeStr):
        typ = typeStr[1]
        strring = u''
        if isinstance(strx, unicode):
            strring = strx
        else:
            strring = str(strx).decode('utf-8')
        # strring = strx
        # strring.strip('"')
        if typ == 's':
            lex = arrayLexer.ArrayLexer()
            list = lex.prase(strring)
            return  list
        else:
            list = strring.split(',')
            for i in range(len(list)):
                if typ == 's':
                    list[i] = list[i]
                elif typ == 'i':
                    list[i] = int(float(list[i]))
                elif typ == 'f':
                    list[i] = float(list[i])

            return list

    # 解析字符串's'类型,因为字符串内部可能包含转意字符,所以需要自己解析
    # eg: 树\\\n\"333
    def __praseStr(self, strx):
        strring = u''
        if isinstance(strx, unicode):
            strring = strx
        else:
            strring = str(strx).decode('utf-8')

        i = 0
        out = ''
        while i < len(strring):
            if strring[i] == '\\':
                nextCh = strring[i+1]
                if nextCh == 'r':
                    pass
                elif nextCh == '"':
                    out += '\"'
                elif nextCh == 'n':
                    out += '\n'
                elif nextCh == 't':
                    out += '\t'
                elif nextCh == '\\':
                    out += '\\'

                i += 2
            else:
                out += strring[i]
                i += 1

        return out

    #转换字符串为dict
    def __convertStrToDict(self, str):
        lex = dictLexer.DictLexer()
        dict = lex.parseText(str)

        return dict

    def log(self):
        print u'类型行', self.typeRow
        print u'配置字段名行', self.cfgNameRow
        print u'中文字段名行', self.chinaNameRow
        print u'数据起始行', self.dataStartRow
        print u'数据终止行', self.dataEndRow
        print u'数据终止列', self.dataEndCol
        print u'字段属性'
        for field in self.fieldList:
            print field

    #获得当前行的recordId,主键
    def __getRecordId(self, row):
        recordId = self.shet.cell(row, 0).value
        ctype = self.shet.cell(row, 0).ctype
        if ctype == XL_CELL_TEXT:
            pass
        elif ctype == XL_CELL_NUMBER:
            #处理为整数做主键
            recordId = int(recordId)
            #TODO 并不支持小数做主键

        return recordId

    #解析自身数据为python
    def __convertPython(self):
        #dump数据#
        for row in range(self.dataStartRow, self.dataEndRow):
            recordId = self.__getRecordId(row)
            record = self.python_obj[recordId] = {}

            for col in range(0, self.dataEndCol):
                field = self.fieldList[col]

                fieldName = field.cfgName
                fieldType = field.type

                value = self.shet.cell(row, col).value

                ctype = self.shet.cell(row, col).ctype

                #如果没有类型字段，就自动判断类型，只支持i、f、s
                if fieldType == '' or fieldType == None:
                    fieldType = self.__autoDecideType(value)

                if fieldType.lower() == 'i':
                    record[fieldName] = int(value)
                elif fieldType == 'f':
                    record[fieldName] = value
                elif fieldType == 's':
                    record[fieldName] = self.__praseStr(value)
                    # record[fieldName] = value
                elif fieldType == 'b':
                    record[fieldName] = bool(value)
                elif fieldType == 'as' or fieldType == 'ai' or fieldType == 'af':
                    record[fieldName] = self.__convertStrToList(value, fieldType)
                elif fieldType == 'd':
                    record[fieldName] = self.__convertStrToDict(value)

    def toPython(self, sheet_output_field=[]):
        # 选择性输出
        if sheet_output_field == []:
            return self.python_obj
        else:
            new_python_obj = self.python_obj.copy()
            for recordId in new_python_obj:
                delFieldNameList = []

                for fieldName in new_python_obj[recordId]:
                    if fieldName in sheet_output_field:
                        pass
                    else:
                        delFieldNameList.append(fieldName)

                for delFieldName in delFieldNameList:
                    del new_python_obj[recordId][delFieldName]

            return new_python_obj

    def __autoDecideType(self,value):
        if isinstance(value,float):
            if math.ceil(value) == value:
                return 'i'
            else:
                return 'f'
        else:
            return 's'

    def toJSON(self):
        sheet_output_field = []
        for col in range(0, self.dataEndCol):
            field = self.fieldList[col]
            fieldUserType = field.userType
            if fieldUserType == 0 or fieldUserType == 1:
                sheet_output_field.append(field.cfgName)

        json_obj = json.dumps(self.toPython(sheet_output_field), sort_keys=True, indent=2, ensure_ascii=False)
        return json_obj

def openSheet(shet):
    return Sheet(shet)