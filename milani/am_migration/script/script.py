# -*- encoding: utf-8 -*-
import os
import csv
import unicodedata
import xmlrpclib
import re
import math

HOST='212.111.40.139'
PORT=8069
#~ DB='AM_Sport_Live'
DB='Live_AM_Sport'
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
        export_file = csv.DictReader(open('/opt/openerp/server/openerp/addons/am_migration/script/partner.csv'))
        count = 0
        #~ partner_ids = object_proxy.execute(DB,uid,PASS,'res.partner','search',[])
        #~ partner = object_proxy.execute(DB,uid,PASS,'res.partner','read',partner_ids,['account_id'])
        #~ for i in partner:
            #~ print '%s -> %s'%(i['account_id'],i['account_id'][0:3]+i['account_id'][4:8])
            #~ object_proxy.execute(DB,uid,PASS,'res.partner','write',[i['id']],{'account_id':i['account_id'][0:3]+i['account_id'][4:8]})
        for line in export_file:
            partner_id = object_proxy.execute(DB,uid,PASS,'res.partner','search',[('name','=',line['name'])])
            city_id = object_proxy.execute(DB,uid,PASS,'city.city','search',[('name','=',line['city_name'])])
            province_id = object_proxy.execute(DB,uid,PASS,'province.province','search',[('name','=',line['province_name'])])
            district_id = object_proxy.execute(DB,uid,PASS,'district.district','search',[('name','=',line['district_name'])])
            if partner_id:
                edit = object_proxy.execute(DB,uid,PASS,'res.partner','write',partner_id,{
                            'activity': line['activity'],
                            'comment': line['comment'],
                            'bio': line['bio'],
                            'brands': line['brands'],
                            'contact_address': line['contact_address'],
                            'city_id': city_id and city_id[0] or '',
                            'district_id': district_id and district_id[0] or '',
                            'entry': line['entry'],
                            'email': line['email'],
                            'entitytype': line['entitytype'],
                            'facebook': line['facebook'],
                            'fax': line['fax'],
                            'fiscal_id': line['fiscal_id'],
                            'call_again': line['call_again'],
                            'google': line['google'],
                            'internal_note': line['internal_note'],
                            'latitude': line['latitude'],
                            'logged_call': line['logged_call'],
                            'longitude': line['longitude'],
                            'mobile': line['mobile'],
                            'name': line['name'],
                            'phone': line['phone'],
                            'product_and_service': line['product_and_service'],
                            'product_summary': line['product_summary'],
                            'province_id': province_id and province_id[0] or '',
                            'schedule_call': line['schedule_call'],
                            'skype': line['skype'],
                            'source': line['source'],
                            'vat': line['vat'],
                            'website': line['website'],
                })
                if edit:
                    count+=1
                    print 'Se ha editado el cliente [%s] %s exitosamente'%(line['account_id'],line['name'])
        print 'records edited:',count

def __main__():
    print 'Began the customer data edition'
    _generate(True)
    print 'Process finished'
__main__()
