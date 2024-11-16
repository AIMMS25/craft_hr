# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LiftingPermit(Document):
	pass

	def validate(self):
		if self.capacity_of_crane and self.capacity_of_crane != 0: 
			self.percentage_crane_utilization = (self.total_lifting_load  / self.capacity_of_crane )* 100

