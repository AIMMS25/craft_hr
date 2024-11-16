# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class SalikAccount(Document):
	pass

	def validate(self):
		self.calculate_total_amount()

	def calculate_total_amount(self):
		opening_balance = self.opening_balance or 0
		total_transaction = self.total_transaction or 0
		total_recharged_amount = self.total_recharged_amount or 0		
		self.balance = (opening_balance - total_transaction) + total_recharged_amount
