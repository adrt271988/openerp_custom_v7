# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import datetime



class company_type(osv.osv):
    _name = 'company.type'
    _columns ={
               'name': fields.char('company type',required=True),
               }
    
class partner_brand(osv.osv):
    _name = 'partner.brand'
    _columns ={
               'name': fields.char('Brand',required=True),
               }

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
                'name': fields.char('Account Name', size=258, required=True, select=True),
                'company_type_original':fields.many2one('company.type','Company Type'),             
                'state_id':fields.many2one('res.country.state','Region'),              
                'relation_name' : fields.char('Relation Name'),
                'portal_code' : fields.char('Portal Code'),
                'subject_type' : fields.char('Subject Type'),
                'business_entity' : fields.char('Business Entity'),
                'fiscal_id' : fields.char('Fiscal Id'),
                'activity_group' : fields.char('Activity Group'),
                'activity' : fields.char('Activity'),
                'product_and_service' : fields.char('Product And Service'),
                'affiliation' : fields.char('Affiliation'),
                'affiliation_id' : fields.char('Affiliation ID'),
                'number_of_ethletor' : fields.integer('Number Of Ethletics'),
                'cat' : fields.char('CAT'),
#*******************************Added by George Vincent**************************************
#Communication
                'skype':fields.char('Skype ID'),
                'google':fields.char('Google +'),
                'facebook':fields.char('Facebook ID'),
                'linkedin':fields.char('LinkedIn ID'),
                'twitter':fields.char('Twitter ID'),
                
                'team_type':fields.boolean('Non-profit'),
                'private':fields.boolean('Private'),
                'account_type':fields.char('Account Type'),
                
                'latitude':fields.char('Latitude'),
                'longitude':fields.char('Longitude'),
                'account_id':fields.char('Account ID'),
                'entitytype' : fields.char('Entity Type'),
#Call Summary
                'logged_call': fields.boolean('Logged Call'),
                'yet_to_log': fields.boolean('First Call'),
                'call_again': fields.boolean('Call Again'),
                'schedule_call': fields.boolean('Schedule Call'),
#Address
                'city_id':fields.many2one('city.city','City'),
                'district_id':fields.many2one('district.district','District'),
                'province_id':fields.many2one('province.province','Province'),
                'second_address_id':fields.many2one('res.partner',"Second address"),
                'third_address_id':fields.many2one('res.partner',"Third address"),
#Additional INFO
                'internal_note':fields.text('Internal Note'),
                'bio':fields.text('Bio'),
                'comment':fields.text('Activity Summary'),
                'product_summary':fields.text('Product Summary'),
#Account Profile fields start
                'prospect':fields.boolean('Prospect'),
                'customer':fields.boolean('Customer'),
                'supplier':fields.boolean('Supplier'),
                'competitor':fields.boolean('Competitor'),
                'other':fields.boolean('Other'),
                
                'production':fields.boolean('Production'),
                'import':fields.boolean('Import'),
                'wholesale':fields.boolean('Wholesale'),
                'retail':fields.boolean('Retail'),
				'rent':fields.boolean('Rent'),
                'repair_assembly':fields.boolean('Repair/Assembly'),
                'activity_other':fields.boolean('Other'),
                'raising':fields.boolean('Racing'),
                'leisure':fields.boolean('Leisure'),
                'urban':fields.boolean('Urban'),
                'free_style':fields.boolean('Free style'),
                'kid':fields.boolean('Kids'),
                'mass_market':fields.boolean('Mass Market'),
                'electric':fields.boolean('Electric'),
                'prod_foc_others':fields.boolean('Other'),
                'annual_revenue':fields.char('Annual Revenue'),
                'number_of_employees':fields.char('Number Of Employees'),
                'foundation_year':fields.datetime('Foundation Year'),
                'brands':fields.char('Brands'),
                'attachment_ids': fields.many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments'),
                'source':fields.char('Source'),
                'count_invoice':fields.integer('Number of Invoice per customer'),
                'count_quotation':fields.integer('Number of Sale per customer'),
#Account Profile fields Ends
#George Vincent's CRM customization code ENDs               
                'default_name':fields.boolean('Person'),
                'competitor':fields.boolean('Competitor'),
                'others_emp':fields.boolean('Other'),
                'prospects':fields.boolean('Prospects'),
                'foundation_year':fields.datetime('Foundation Year'),
                'entry':fields.selection([('1','Sale-Proprietorship'),('2','Partnership'),('3','Limited Liability Company'),('4','Corporation'),('5','Non-Profit')],'Entry :',invisible=1),
                'major_brands':fields.many2many('partner.brand','partner_brand_rel','partner_id','brand_id','Major Brands'),
                'unit_sale_m':fields.float('Unit Sales / YR'),
                'sport':fields.selection([('cycle','Cycling'),('triathlon','Triathlon'),('othersport','Other')],'Sport',invisible=True,),
                'created_on':fields.datetime('Created On'),
                'modified_on':fields.datetime('Last-Modified On'),
                'created_by':fields.many2one('res.users','Created By'),
                'modified_by':fields.many2one('res.users','Last-Modified By'),
                'vat': fields.char('VAT/Tax ID', help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
                'presentation':fields.binary('Company Presentation'),
                'logoes':fields.binary('Logo'),
                'skype':fields.char('Skype ID'),
                'affiliation':fields.char('Affiliation'),
                'team_registration':fields.char('Team Registration'),

                'team':fields.boolean('Team'),
                'sponsor':fields.boolean('Sponsor'),
                'triathlon':fields.boolean('Triathlon'),
                'road' : fields.boolean('Road'),
                'mtb_speciality':fields.boolean('MTB'),
                'cross_speciality' :fields.boolean('Cross'),
                'junior' :fields.boolean('Junior'),
                'adults' :fields.boolean('Adults'),
                'recreational' :fields.boolean('Recreational'),
                'pro_type' :fields.boolean('Pro'),
                'school_type' :fields.boolean('School'),
                'competitive' :fields.boolean('Competitive'),
                
                'market_leader':fields.boolean('Market Leader'),
                'second_tier':fields.boolean('2nd Tier'),
                'small_shop':fields.boolean('Small Shop'),
                'other_market':fields.boolean('Other'),
                }
    _defaults = {
                    'prospects': True,                  
                    'default_name': True,
                    'customer': False,
                    'account_id': lambda obj, cr, uid, context: '',
                }
    _sql_constraints = [
        ('account_id', 'unique(account_id)', 'Customer Reference must be unique'),
    ]
        
    
    def open_map(self, cr, uid, ids, context=None):
        address_obj= self.pool.get('res.partner')
        partner = address_obj.browse(cr, uid, ids, context=context)[0]
        url="http://maps.google.com/maps?oi=map&q="
         
        if partner.latitude:
            lati = str(partner.latitude)  
            url+=lati.replace(' ','+')
        if partner.longitude:
            lon = str(partner.longitude)  
            url+='+'+lon.replace(' ','+')
        return {
                'type': 'ir.actions.act_url',
                'url':url,
                'target': 'new'
               }     
        
    def get_select(self, cr, uid, ids,is_company, team_type, default_name,context=None):
        val = {}
        if is_company == True:
            val = {
                      'default_name' : False,
                      'team_type': False,
                      'entry' : 'Select',                     
                     }
            return {'value' : val}
        
        elif team_type == True :                
            val = {
                      'is_company' : False,
                      'default_name' : False,
                      'entry' : '5',
                      'sport' : 'Select',
                     }            
            return {'value' : val}
        
        elif team_type == False and is_company == False:
            val = {
                      'default_name' : True,
                        
                    }
            return {'value' : val}
        return True
    
    def onchange_team_type(self, cr, uid, ids,team_type,context=None):
        val = {}
        if team_type == True:
            val = {
                      'is_company' : False,
                      'private' : False,
                      'account_type':'Business',
                   }
        return {'value' : val}
    
    def onchange_company(self, cr, uid, ids,is_company,context=None):
        val = {}
        if is_company == True:
            val = {
                      'team_type' : False,
                      'private' : False,
                      'account_type':'Non-profit',
                   }
        return {'value' : val}
    
    def onchange_private(self, cr, uid, ids,private,context=None):
        val = {}
        if private == True:
            val = {
                      'team_type' : False,
                      'is_company' : False,
                      'account_type':'Private',
                   }
        return {'value' : val}

    
    def write(self, cr, uid, ids, vals, context=None):
        
        if isinstance(ids, (int, long)):
            ids = [ids]
        result = super(res_partner,self).write(cr, uid, ids, vals, context=context)
        for partner in self.browse(cr, uid, ids, context=context):
            self._fields_sync(cr, uid, partner, vals, context)
        date = datetime.datetime.now()
        if ids:
            cr.execute(""" update res_partner set modified_on=%s,modified_by=%s where id=%s""",(date,uid,ids[0],))
        return result

    def create(self, cr, uid, vals, context=None):
        if not vals.get('account_id'):
            vals['account_id'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner')
            
        new_id = super(res_partner, self).create(cr, uid, vals, context=context)
        partner = self.browse(cr, uid, new_id, context=context)
        self._fields_sync(cr, uid, partner, vals, context)
        self._handle_first_contact_creation(cr, uid, partner, context)
        
        date = datetime.datetime.now()
        cr.execute(""" update res_partner set created_on=%s,modified_on=%s,created_by=%s,modified_by=%s where id=%s""",(date,date,uid,uid,new_id,))
        
#          ************* Commented BY George Vincent ********************
#        vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner')
#        cr.execute(""" update res_partner set ref=%s where id=%s""",(vals['ref'],new_id,))
        return new_id
    
class sale_order(osv.osv):
    _inherit = 'sale.order'    
    _columns={
              }
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
            m=super(sale_order, self).create(cr, uid, vals, context=context)
            cr.execute(""" select partner_id from sale_order where id=%s""",(m,))
            partner_id = cr.fetchall()
            cr.execute(""" update res_partner set customer='true',prospects='false' where id=%s""",(partner_id[0][0],))
        return m#super(sale_order, self).create(cr, uid, vals, context=context)

class purchase_order(osv.osv):
    _inherit = 'purchase.order'    
    _columns={
              }
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order') or '/'
            order =  super(purchase_order, self).create(cr, uid, vals, context=context)
            cr.execute(""" select partner_id from purchase_order where id=%s""",(order,))
            partner_id = cr.fetchall()
            cr.execute(""" update res_partner set supplier='true',prospects='false' where id=%s""",(partner_id[0][0],))
        return order
    
class res_partner_title(osv.osv):
    _inherit = 'res.partner.title'
    _columns = {
                    'code_person': fields.boolean('Person'),
                    'code_company': fields.boolean('Company'),
                    'code_sport': fields.boolean('Sport'),                    

                }
    
class Country(osv.osv):
    _inherit = 'res.country'
    _columns = {
                 'vat_type':fields.char('Applied VAT B2B', required=True),
                 'vat_type_two':fields.char('Applied VAT B2C', required=True),
                }
    _defaults = {
        'vat_type': "0%",
        'vat_type_two': "0%",
    }
    

#Helps to create address 
class province_province(osv.osv):    
    _name = 'province.province'
    _columns = {
                 'name':fields.char('Name', required=True),
                 'country_id': fields.many2one('res.country', 'Country'),
                }
    
class CountryState(osv.osv):
    _inherit = 'res.country.state'   
    _columns = {
                'name':fields.char('Name', required=True),
                'code':fields.char('State code'),
                 'province_id':fields.many2one('province.province','Province'),
                 'country_id':fields.many2one('res.country','Country'),
                } 

    
class district_district(osv.osv):    
    _name = 'district.district'
    _columns = {
                 'name':fields.char('Name', required=True),
                 'state_id':fields.many2one('res.country.state','State'),
                 'province_id':fields.many2one('province.province','Province'),
                 'country_id': fields.many2one('res.country', 'Country'),
                }   
    
class city_city(osv.osv):    
    _name = 'city.city'
    _order = 'name'
    _columns = {
                 'name':fields.char('Name', required=True),
                 'district_id':fields.many2one('district.district','District'),
                 'state_id':fields.many2one('res.country.state','State'),
                 'province_id':fields.many2one('province.province','Province'),
                 'country_id': fields.many2one('res.country', 'Country'),
                }
    

                
