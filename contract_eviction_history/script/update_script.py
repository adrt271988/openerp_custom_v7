# -*- encoding: utf-8 -*-
import os
import csv
import unicodedata
import xmlrpclib
import re
import math

HOST = raw_input("Ingrese HOST / IP:\n")
PORT = raw_input("Ingrese Puerto RPC de Odoo/OpenERP:\n")
DB = raw_input("Ingrese Nombre de la Base de Datos:\n")
USER = raw_input("Ingrese Usuario Admin de la Base de Datos:\n")
PASS = raw_input("Ingrese Password de Usuario Admin:\n")
url ='http://%s:%d/xmlrpc/' % (HOST,int(PORT))


common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')
uid = common_proxy.login(DB,USER,PASS)

def _generate(state):
    if state is True:
        rule_codes = ['PROV FOND RESERV','PROV FOND RESERV RE','PROV FOND RESERV RE1']
        
        python_condition = "if contract.validate_f==True:\n\tif contract.contract_history == True or payslip.time_in >= 1:\n\t\tresult = True\nelse:\n\tresult=True"
        for code in rule_codes:
            rule_id = object_proxy.execute(DB,uid,PASS,'hr.salary.rule','search',[('code','=',code)])
            if rule_id:
                object_proxy.execute(DB,uid,PASS,'hr.salary.rule','write',rule_id,{'condition_python':python_condition})
                print 'Se ha editado la regla %s exitosamente'%(code)

def __main__():
    _generate(True)
    print 'Proceso finalizado!!!'
__main__()
