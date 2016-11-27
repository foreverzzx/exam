#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年11月20日
工具模块
@author: dell
'''
import jsonpickle


'''
对象转json
'''
def objtojson(obj):
    return jsonpickle.encode(obj)

'''
must_params表示接口必须要有的参数，args代表页面传过来的参数可直接传web.input()
'''
def paramsok(must_params,args):
    for k in args:
        if k not in args:
            return Status.__params_not_ok__
    return Status.__params_ok__

'''
md5散列
'''
def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

'''
对接口状态进行定义
'''
class Status:
    __success__ = 1 #操作成功
    __error__ = 0 #操作失败
    __params_not_ok__ = 2 #参数传递错误
    __params_ok__ = 3 #参数传递正确
    __not_login__ = 4 #还未登陆
    __password_not_match__ = 5 #密码错误
    __obj_null__ = 6 #对象为空
    __system_exception = 7 #程序抛出异常
    __not_exist__ = 8 #不存在        

'''
对不需要使用分页的接口返回数据进行封装
status:接口返回状态,message:接口状态描述,body:返回数据
'''
class Response:
    def __init__(self,status = Status.__error__,message = "未知",body = None):
        self.status = status
        self.body = body
        self.message = message

'''
data:要填充的数据，如{"id":1,"name":"ajj"}
totalRow:总条数，
currentPage:当前请求页，pageSize:每页显示数目，
status:返回状态，在Status类中定义了各种状态类型
message:状态信息描述
'''
class Page:
    def __init__(self,data,totalRow,currentPage,pageSize = 10,status = Status.__error__,message = "未知"):
        self.totalRow = totalRow
        self.data = data
        self.currentPage = int(currentPage)
        self.pageSize = pageSize
        self.totalPage = totalRow/pageSize if (totalRow%pageSize == 0) else (totalRow/pageSize + 1)#总页数
        self.firstPage = self.currentPage == 1#是否为第一页
        self.lastPage = self.currentPage == self.totalPage #是否为最后一页
        self.status = status
        self.message = message

'''
test和write两个函数配合自动生成model类，建立与数据库之间的联系
'''
def test(db,file_name):
        file = open(file_name,'w')   
        sql_tables = 'show tables'
        sql_columns = 'select * from information_schema.COLUMNS where table_name = "%s"'
        sql_pri_column = 'select COLUMN_KEY,COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name="%s" AND COLUMN_KEY="PRI"'
        sql_not_null_column = 'select * from INFORMATION_SCHEMA.COLUMNS where table_name= "%s" and IS_NULLABLE = "NO"'
        tables = db.query(sql_tables)
        for table in tables:
            __table__ = "'" + str(table['Tables_in_examdb']) + "'"
            table1 = table['Tables_in_examdb']  
            __pk__ = db.query('select COLUMN_KEY,COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name=%s AND COLUMN_KEY="PRI"' % __table__)[0]['COLUMN_NAME']
            __notnull__ = "set({"
            columns = db.query('select * from information_schema.COLUMNS where table_name = %s' % __table__)
            __attrnum__ = len(columns)
            print __attrnum__
            __attr__  = "set(["
            __updateable__ = __insertable__ = "set({" 
            __countperpage__ = 10
            for column in columns:
                column_name = column['COLUMN_NAME']
                __attr__ += "'" + column_name + "',"
                
                __insertable__ += ("'" + column_name + "',") if column_name != __pk__ else ""
                __updateable__ += ("'" + column_name + "',") if column_name != __pk__ else ""
                __notnull__ += ("'" + column_name + "',") if column['IS_NULLABLE'] == 'NO' and column_name != __pk__ else ""
            __attr__ += "])"
            __insertable__ += "})"
            __updateable__ += "})"
            __notnull__ += "})"

            write(file,table1,__pk__,__attr__,__insertable__,__updateable__,__notnull__)
            file.write('\n')
        file.close()
'''
配合上述test函数
'''        
def write(file,__table__,__pk__,__attr__,__insertable__,__updateable__,__notnull__):
    file.write("class "+ __table__[0].upper() + __table__[1:] + '_model(Model):\n')  
    file.write("    __table__ = '" + __table__ + "'\n")
    file.write("    __pk__ = '" + __pk__ + "'\n")
    file.write('    __attr__ = ' + __attr__ + "\n")
    file.write('    __insertable__ = ' + __insertable__ + "\n")
    file.write('    __updateable__ = ' + __updateable__ + "\n")
    file.write('    __notnull__ = ' + __notnull__ + "\n")
    file.write('    __attrnum__ = len(__attr__)' + "\n")
    file.write('    __countperpage__ = 10' + "\n")
