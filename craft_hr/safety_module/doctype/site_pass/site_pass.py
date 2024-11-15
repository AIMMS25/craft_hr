# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import datetime



class SitePass(Document):
    def validate(self):
        if self.date and self.site_pass_expiry:
            date_obj = datetime.strptime(self.date, '%Y-%m-%d')
            expiry_obj = datetime.strptime(self.site_pass_expiry, '%Y-%m-%d')

            remaining_days = (expiry_obj - date_obj).days
            
            self.remaining_days = remaining_days
        else:
            self.remaining_days = 0

