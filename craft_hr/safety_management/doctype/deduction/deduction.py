# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Deduction(Document):
	pass


	def on_submit(self):
		if self.deduction_amount > 0:
			additional_salary = frappe.new_doc('Additional Salary')
			additional_salary.employee = self.employee
			additional_salary.salary_component = "Violation Deduction"
			additional_salary.amount = self.deduction_amount
			additional_salary.payroll_date = self.registering_date
			additional_salary.company = self.company
			additional_salary.insert()
			additional_salary.submit()

			frappe.msgprint(
				msg=f"Additional Salary created for Employee {self.emp_id}",
				alert=True
			)

