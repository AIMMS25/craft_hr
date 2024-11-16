# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AddSalikExpense(Document):
    pass

@frappe.whitelist()
def create_salik_expenses(trip_details):
    import json
    trip_details = json.loads(trip_details)
    
    for row in trip_details:
        amount = row.get('amount', 0)
        
        if amount and amount > 0:
            salik_expense = frappe.get_doc({
                'doctype': 'Salik Expense',
                'account_no': row.get('account_no', ''),
                'transaction_id': row.get('transaction_id', ''),
                'trip_date': row.get('trip_date', ''),
                'trip_time': row.get('trip_time', ''),
                'transaction_post_date': row.get('transaction_post_date', ''),
                'toll_gate': row.get('toll_gate', ''),
                'direction': row.get('direction', ''),
                'tag_number': row.get('tag_number', ''),
                'vehicle': row.get('vehicle', ''),
                'amount': amount,
                'company': row.get('company', ''),
                'odometer': row.get('odometer', 0),
                'posting_date' :row.get('transaction_post_date','')
            })
            salik_expense.insert()
            salik_expense.submit()
    
    return True
