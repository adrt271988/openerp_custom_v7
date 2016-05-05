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
        export_file = csv.DictReader(open('/opt/openerp/server/openerp/addons/am_migration/data/product.csv'))
        #~ export_file = csv.DictReader(open('/home/openerp/instancias/7.0/milani/am_migration/data/product.csv'))
        count = 0
        for line in export_file:
            if line['color_id']=='ORN':
                product_id = object_proxy.execute(DB,uid,PASS,'product.product','search',[('default_code','=',line['internal_ref_id'])])
                color_id = object_proxy.execute(DB,uid,PASS,'color.master','search',[('name','=','ORG')])
                if product_id:
                    edit = object_proxy.execute(DB,uid,PASS,'product.product','write',product_id,{'color_id':color_id and color_id[0] or ''})
                    if edit:
                        count+=1
                        print 'Se ha editado el producto [%s] exitosamente'%(line['internal_ref_id'])
        print 'records edited:',count

def __main__():
    print 'Began the product data edition'
    _generate(True)
    print 'Process finished'
__main__()
