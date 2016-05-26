# -*- encoding: utf-8 -*-
import os
import csv
import unicodedata
import xmlrpclib
import re
import math

HOST='212.111.40.139'
PORT=8069
DB='AM_Sport_Live'
USER='admin'
PASS='AmSpOrt90'
url ='http://%s:%d/xmlrpc/' % (HOST,PORT)
#~ HOST='localhost'
#~ PORT=8069
#~ DB='am_sports_4'
#~ USER='admin'
#~ PASS='12345'
#~ url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _generate(state):
    if state is True:
        #~ product_id = object_proxy.execute(DB,uid,PASS,'product.product','search',[('name','=','LIMITED 3.0')])
        #~ product_id = object_proxy.execute(DB,uid,PASS,'product.product','search',[('name','=','LIGHT 3.0')])
        product_id = object_proxy.execute(DB,uid,PASS,'product.product','search',[('name','=','EXTREME 3.0')])
        if product_id:
            for i in product_id:
                #~ object_proxy.execute(DB,uid,PASS,'product.product','write',[i],{'standard_price':105.40})
                object_proxy.execute(DB,uid,PASS,'product.product','write',[i],{'x_factor':2.1326})

def __main__():
    print 'Began the product data edition'
    _generate(True)
    print 'Process finished'
__main__()
