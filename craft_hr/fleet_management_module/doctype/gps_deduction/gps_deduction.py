# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GPSDeduction(Document):
	pass

	def on_submit(self):
		if self.amount > 0 and self.employee:
			additional_salary = frappe.new_doc('Additional Salary')
			additional_salary.employee = self.employee
			additional_salary.salary_component = "GPS Deduction"
			additional_salary.amount = self.amount
			additional_salary.payroll_date = self.date
			additional_salary.company = self.company
			additional_salary.insert()
			additional_salary.submit()

			frappe.msgprint(
				msg=f"Additional Salary created for Employee {self.employee}",
				alert=True
			)