#xlsx2jsonpy
python, Excel文件转化为json的小工具

网上有很多这类的工具，但是跟自己的需求并不能完全匹配，所以还是决定自己动手写一个，这个工具参考了很多网上开源的项目，详细请看最下面参考文案。

##环境
-   Python 2.7
-   xlrd

##字段类型
字段类型是必选标记。支持如下的字段类型：

-   s：字符串

-   i：整数

-   f：小数

-   b：布尔

-   as：字符串数组
>####数据格式(类似：`"\"a\\\ne\"r",dd,a`)
> 1. 使用 half-angle
> 2. 使用 **,** to split array data 
> 3. 如果字符串内部需要使用 `,`, 则必须使用双引号把整个字符包裹

-   ai：整数数组

-   af：小数数组

-   d：字典，若在字典中想使用数字字符串作为值，请在数字两端加""
> 逗号分割，键值对使用 : 

##使用
```
python xlsx2json.py -i 配置目录 -o 输出目录
```
#参考
1.[https://github.com/gdgoldlion/ExcelAndJSON](https://github.com/gdgoldlion/ExcelAndJSON)  
2. [https://github.com/zhangqi-ulua/XlsxToLua/blob/master/XlsxToLua%E5%B7%A5%E5%85%B7%E8%AF%B4%E6%98%8E.txt](https://github.com/zhangqi-ulua/XlsxToLua/blob/master/XlsxToLua%E5%B7%A5%E5%85%B7%E8%AF%B4%E6%98%8E.txt)
3. [https://github.com/Eddie104/Libra-lua/tree/master/tools/xls2lua](https://github.com/Eddie104/Libra-lua/tree/master/tools/xls2lua)  
4. [https://github.com/dongdongcpk/xlsx2json-py](https://github.com/dongdongcpk/xlsx2json-py)


