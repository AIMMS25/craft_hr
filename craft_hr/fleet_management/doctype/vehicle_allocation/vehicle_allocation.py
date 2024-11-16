# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VehicleAllocation(Document):
	pass

	def validate(self):
		self.check_vehicle_availability()

	def check_vehicle_availability(self):
		allocations = frappe.db.sql("""
			SELECT name FROM `tabVehicle Allocation`
			WHERE vehicle=%s 
			AND (
				(from_date <= %s AND to_date >= %s) 
				OR (from_date <= %s AND to_date >= %s)
			)
			AND name != %s
		""", (self.vehicle, self.from_date, self.from_date, self.to_date, self.to_date, self.name))

		if allocations:
			frappe.throw(frappe._("This vehicle is already allocated within the selected date range."))
