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
        export_file = csv.DictReader(open('/opt/openerp/server/openerp/addons/am_product/data/prices.csv'))
        #~ export_file = csv.DictReader(open('/home/openerp/instancias/7.0/milani/am_product/data/prices.csv'))
        for line in export_file:
            object_proxy.execute(DB,uid,PASS,'product.product','write',[int(line['product_id'])],{'list_price':float(line['list_price'])})
            print 'Product %s has been edited'%line['product_id']

def __main__():
    print 'Began the product data edition'
    _generate(True)
    print 'Process finished'
__main__()
