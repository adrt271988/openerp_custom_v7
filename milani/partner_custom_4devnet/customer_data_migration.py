from openerp.osv import fields, osv
import base64
import xlrd
import xlwt
import sys
import os
import urllib
from tempfile import TemporaryFile
import requests

#File import save this in local path
file_path = 'opt/openerp/server/openerp/addons/partner_custom_4devnet/customer_data/Customer_data.xlsx'

class customer_data_migration(osv.osv):
    _name = 'customer.data.migration'
    _description = 'Customer Data Migration'
    
    _columns={
        'file': fields.binary('File'),
    }

    def format_cell_value(self, val):
        v = None
        if isinstance(val, float) or isinstance(val, int):
            v = str(int(val))
        else:
            v = str(val)
        return v
    
    def create(self, cr, uid, vals, context=None):

        module_data = vals.get('file',None)
        if module_data:
#            Decode file that is uploaded
            decoded_data = base64.decodestring(module_data)
#            Get os path to store file in local system
#            file_path = os.path.join(str(os.getcwd())+ os.sep, 'openerp'+ os.sep, 'addons' + os.sep, 'partner_custom_4devnet' + os.sep, 'customer_data' + os.sep,"Customer_data.xlsx")
            f = open(file_path, "wb")
#            Write file Data
            f.write(decoded_data)
            f.close()
#            Get file and get dtafault fist sheet vaue
            workbook = xlrd.open_workbook(file_path)
            worksheet = workbook.sheet_by_index(0)
            temp=vals
            # read header values into the list    
            keys = [worksheet.cell(0, col_index).value for col_index in xrange(worksheet.ncols)]
            #Make Dictionay based on Kye values fixed on first row
            for row_index in xrange(1, worksheet.nrows):
                dict_list = {keys[col_index]: worksheet.cell(row_index, col_index).value for col_index in xrange(worksheet.ncols)}
                vals={}
                if dict_list.get('name',None):
#                    Get list of values from dictionary
                    logoes=dict_list.get('logoes',None)
                    image=dict_list.get('image',None)
                    source=dict_list.get('source',None)
                    longitude=dict_list.get('longitude',None)
                    latitude=dict_list.get('latitude',None)
                    comment=dict_list.get('comment',None)
                    raising=dict_list.get('raising',None)
                    product_summary=dict_list.get('product_summary',None)
                    street=dict_list.get('street',None)
                    zip=dict_list.get('zip',None)
                    city_name=dict_list.get('city_id',None)
                    province_name=dict_list.get('province_id',None)
                    state_name=dict_list.get('state_id',None)
                    vat=dict_list.get('vat',None)
                    fiscal_id=dict_list.get('fiscal_id',None)
                    country_name=dict_list.get('country_id',None)
                    district_name=dict_list.get('district_id',None)
                    phone=dict_list.get('phone',None)
                    mobile=dict_list.get('mobile',None)
                    fax=dict_list.get('fax',None)
                    website=dict_list.get('website',None)
                    email=dict_list.get('email',None)
                    facebook=dict_list.get('facebook',None)
                    bio=dict_list.get('bio',None)
                    is_company=dict_list.get('is_company')
                    team_type=dict_list.get('team_type')
                    private=dict_list.get('private')
                    entitytype=dict_list.get('entitytype',None)
                    annual_revenue=dict_list.get('annual_revenue',None)
                    number_of_employees=dict_list.get('number_of_employees',None)
                    brands=dict_list.get('brands',None)
                    foundation_year=dict_list.get('foundation_year',None)
                    competitor=dict_list.get('competitor')
                    property_account_receivable=dict_list.get('property_account_receivable',None)
                    property_account_payable=dict_list.get('property_account_payable',None)
#                    Validate field data and update values
                    vals.update({
                         'name': dict_list.get('name'),
                         'prospect': True
                         })
                    if image:
                        response = requests.get(image)
                        image=base64.b64encode(response.content)
                        vals.update({
                                 'image': image
                                 })
                    if logoes:
                        logoes_response = requests.get(logoes)
                        logoes=base64.b64encode(logoes_response.content)
                        vals.update({
                                 'logoes': logoes
                                 })
                    if source: 
                        vals.update({
                                 'source': source
                                 })
                    if longitude: 
                        vals.update({
                                 'longitude': longitude
                                 })
                    if latitude: 
                        vals.update({
                                 'latitude': latitude
                                 })
                    if comment: 
                        vals.update({
                                 'comment': comment
                                 })
                    if product_summary: 
                        vals.update({
                                 'product_summary': product_summary
                                 })
                    if street: 
                        vals.update({
                                 'street': street
                                 })
                    if zip:
                        vals.update({
                                 'zip': zip
                                 })
#        Look for the city,province,state,district and country name and return the record id
                    if city_name:
                        city_id = self.pool.get('city.city').search(cr, uid, [('name','=',city_name)], context=context)
                        if city_id:
                            vals.update({
                                     'city_id': city_id[0]
                                     })
                        else:
                            city_val={}
                            city_val.update({
                                     'name': city_name
                                     })
                            city_id=self.pool.get('city.city').create(cr, uid, city_val, context=context)
                            vals.update({
                                     'city_id': int(city_id)
                                     })
                    if province_name: 
                        province_id = self.pool.get('province.province').search(cr, uid, [('name','=',province_name)], context=context)
                        if province_id:
                            vals.update({
                                     'province_id': province_id[0]
                                     })
                        else:
                            province_val={}
                            province_val.update({
                                     'name': province_name
                                     })
                            province_id=self.pool.get('province.province').create(cr, uid, province_val, context=context)
                            vals.update({
                                     'province_id': int(province_id)
                                     })
                    if state_name: 
                        state_id = self.pool.get('res.country.state').search(cr, uid, [('name','=',state_name)], context=context)
                        if state_id:
                            vals.update({
                                     'state_id': state_id[0]
                                     })
                        else:
                            state_val={}
                            state_val.update({
                                     'name': state_name,
                                     'code': state_name[:2],
                                     })
                            state_id=self.pool.get('res.country.state').create(cr, uid, state_val, context=context)
                            vals.update({
                                     'state_id': int(state_id)
                                     })
                    if district_name: 
                        district_id = self.pool.get('district.district').search(cr, uid, [('name','=',district_name)], context=context)
                        if district_id:
                            vals.update({
                                     'district_id': district_id[0]
                                     })
                        else:
                            district_val={}
                            district_val.update({
                                     'name': district_name
                                     })
                            district_id=self.pool.get('district.district').create(cr, uid, district_val, context=context)
                            vals.update({
                                     'district_id': int(district_id)
                                     })
                            
                    if country_name: 
                        country_id = self.pool.get('res.country').search(cr, uid, [('name','=',country_name)], context=context)
                        if country_id:
                            vals.update({
                                     'country_id': country_id[0]
                                     })
                        else:
                            country_val={}
                            country_val.update({
                                     'code': country_name[:2],
                                     'vat_type': '22%',
                                     'vat_type_two': '22%',
                                     'name': country_name
                                     })
                            country_id=self.pool.get('res.country').create(cr, uid, country_val, context=context)
                            vals.update({
                                     'country_id': int(country_id)
                                     })
                        
                    if vat:
                        vals.update({
                                 'vat':vat
                                 })
                            
                    if fiscal_id:
                        vals.update({
                                 'fiscal_id': fiscal_id
                                 })
                    if phone: 
                        vals.update({
                                 'phone': phone
                                 })
                    if mobile: 
                        vals.update({
                                 'mobile': mobile
                                 })
                        
                    if fax:
                        vals.update({
                                 'fax': fax
                                 })
                    if website: 
                        vals.update({
                                 'website': website
                                 })
                    if email: 
                        vals.update({
                                 'email': email
                                 })
                    if facebook: 
                        vals.update({
                                 'facebook': facebook
                                 })
                    if bio: 
                        vals.update({
                                 'bio': bio
                                 })
                    if team_type:
                        if team_type=='True' or team_type=='TRUE':
                            vals.update({
                                 'account_type':'Business',
                                 'team_type': team_type
                                 })
                    if private:
                        if private=='True' or private=='TRUE':
                            vals.update({
                                 'account_type':'Private',
                                 'private': private
                                 })
                    if raising:
                        if raising=='True' or raising=='TRUE':
                            vals.update({
                                 'raising': True
                                 })
                    if is_company:
                        if is_company == 'True' or is_company=='TRUE'  :
                            vals.update({
                                 'account_type':'Business',
                                 'is_company': is_company
                                 })
                        
                    if entitytype: 
                        vals.update({
                                 'entitytype': entitytype
                                 })
                    if annual_revenue: 
                        vals.update({
                                 'annual_revenue': annual_revenue
                                 })
                    if brands: 
                        vals.update({
                                 'brands': brands
                                 })
                    if foundation_year: 
                        vals.update({
                                 'foundation_year': foundation_year
                                 })
                    if competitor:
                        if competitor == 'True' or competitor=='TRUE' :
                            vals.update({
                                 'competitor': competitor
                                 })
                    if property_account_receivable:
                        property_account_receivable_id = self.pool.get('account.account').search(cr, uid, [('name','=',property_account_receivable)], context=context)
                        vals.update({
                                 'property_account_receivable': property_account_receivable_id
                                 })
                    if property_account_payable:
                        property_account_payable_id = self.pool.get('account.account').search(cr, uid, [('name','=',property_account_payable)], context=context)
                        vals.update({
                                 'property_account_payable': property_account_payable_id
                                 })
                    if number_of_employees:
                        vals.update({
                                 'number_of_employees': number_of_employees
                                 })
                    if vals:
                        self.pool.get('res.partner').create(cr, uid, vals, context=context)
            vals=temp
        return super(customer_data_migration, self).create(cr, uid, vals, context=context)


customer_data_migration()
