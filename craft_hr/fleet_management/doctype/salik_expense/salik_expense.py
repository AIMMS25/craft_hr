# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class SalikExpense(Document):
    pass

    def on_submit(self):
        self.create_vehicle_log_entry()

        salik_account = frappe.get_doc('Salik Account', {'account_no': self.account_no})

        if salik_account:
            vehicle_doc = frappe.get_doc('Vehicle', self.vehicle)

            if vehicle_doc.custom_account_no == salik_account.account_no:
                available_balance = salik_account.opening_balance + salik_account.total_recharged_amount
                if salik_account.total_transaction > available_balance:
                    frappe.throw('Your total transaction exceeds the available balance. Please recharge your account.')

                if self.amount and self.amount > 0:
                    total_transaction_amount = salik_account.total_transaction + self.amount
                    salik_account.total_transaction = total_transaction_amount
                    salik_account.save()

                    frappe.msgprint(
                        msg='Salik Account total transaction amount updated successfully.',
                        indicator='green',
                        alert=True
                    )



    def on_cancel(self):
        salik_account = frappe.get_doc('Salik Account', {'account_no': self.account_no})
        
        if salik_account:
            total_transaction_amount = salik_account.total_transaction - self.amount
            salik_account.total_transaction = total_transaction_amount
            salik_account.save()


    def create_vehicle_log_entry(self):
        if self.vehicle and self.amount:
            vehicle_log = frappe.new_doc('Vehicle Log')
            vehicle_log.license_plate = self.vehicle
            vehicle_log.odometer = self.odometer
            vehicle_log.date = self.posting_date

            vehicle_log.append('custom_expense', {
                'expense_category': 'Salik Expense',
                'amount': self.amount
            })

            vehicle_log.save()
            vehicle_log.submit() 

            frappe.msgprint(
                            msg=f'Vehicle Log has been created successfully.',
                            indicator='green',
                            alert=True
                        )