# Copyright (c) 2024, Craftinteractive and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EmploymentContractRenewal(Document):
	def before_validate(self):
		new_total = (self.basic_pay or 0) + (self.hra_pay or 0) + (self.transport_allowance_pay or 0) + (self.others_pay or 0)
		self.total_pay =  new_total