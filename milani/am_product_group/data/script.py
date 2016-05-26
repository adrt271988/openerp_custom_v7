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
#~ DB='am_sports_db4'
#~ USER='admin'
#~ PASS='AmSpOrt90'
#~ url ='http://%s:%d/xmlrpc/' % (HOST,PORT)

common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _generate(state):
    if state is True:
        product_ids = object_proxy.execute(DB,uid,PASS,'product.product','search',[])
        products = object_proxy.execute(DB,uid,PASS,'product.product','read',product_ids,['name'])
        for p in products:
			attribute_id = object_proxy.execute(DB,uid,PASS,'product.attribute','search',[('name','=',p['name'])])
			if attribute_id:
				object_proxy.execute(DB,uid,PASS,'product.product','write',[p['id']],{'attribute_id':attribute_id[0]})
				print 'Product %s has been edited'%p['id']

def __main__():
    print 'Began the product data edition'
    _generate(True)
    print 'Process finished'
__main__()
