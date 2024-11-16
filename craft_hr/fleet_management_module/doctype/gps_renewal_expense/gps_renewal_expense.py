# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class GPSRenewalExpense(Document):
	pass


	def validate(self):
		self.amount = (self.charges_per_vehicle or 0) + (self.annual_charges or 0) + (self.sim_charge or 0)

