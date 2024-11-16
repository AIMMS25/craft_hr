# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalikRecharge(Document):
    pass

    def on_submit(self):
        salik_account = frappe.get_doc('Salik Account', {'account_no': self.salik_account_no})
        
        if salik_account:
            recharged_amount = salik_account.total_recharged_amount + self.total_amount
            salik_account.total_recharged_amount = recharged_amount
            salik_account.save()
            
            frappe.msgprint(
                msg=f'Salik Account total recharged amount updated successfully.',
                indicator='green',
                alert=True
            )

    def on_cancel(self):
        salik_account = frappe.get_doc('Salik Account', {'account_no': self.salik_account_no})
        
        if salik_account:
            recharged_amount = salik_account.total_recharged_amount - self.total_amount
            salik_account.total_recharged_amount = recharged_amount
            salik_account.save()
