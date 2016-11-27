#!/usr/bin/env python
# -*- coding: utf-8 -*-


import web

from model.model import Strategy_model
import util


urls = (
    '/1','index',
    
)
        
class index:
    #分页示例
    def GET(self):
        #must_params = ('name','id')
        params = web.input()#通过web.input()获取的值为unicode编码，最好转码为utf-8
        requestPage = params['requestPage'].encode('utf-8')
        lists = Strategy_model.getByArgs()
        print "session",session.status
        data = []
        for each in lists:
            each_data = [each['sg_name'],each['sg_score']]
            data.append(each_data)
        return util.objtojson(util.Page(data, len(lists),requestPage))
        
    def POST(self):
        pass
    
web.config.debug = False
app = web.application(urls, globals())
if web.config.get("_session") is None:
    store = web.session.DiskStore('sessions')
    user = web.utils.Storage({
                          "id": "",#id，
                          "name": "",#姓名
                          "type": "",#用户类型
                          "cla_id":"",#若为学生，班号
                          "privilege": "",#权限
                          "cla_name":"",#若为学生，班名
                          })
    session = web.session.Session(app, store, 
                                  initializer={
                                               "status": 0,
                                               "user": user,
                                               })
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('template')
if __name__ == '__main__':
    
    if len(urls)&1 == 1:
        print "urls error, the size of urls must be even."
    else:
        app.run()

