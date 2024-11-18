# Copyright (c) 2024, ashari k k and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
class DocumentDetails(Document):

	def validate(self):
		if self.is_employee_document:
			if not self.employee:
				frappe.throw("Please select the employee")
			else:
				emp = frappe.get_doc("Employee",self.employee)
				not_existing = 0
				for document in emp.custom_additional_documents:
					if self.document_name.lower() == document.document_name.lower():
						not_existing == 1
				if not_existing == 0:
					print("------")
					emp.append("custom_additional_documents",{
						"document_name" : self.document_name,
						"expiry_date" : self.document_expiry_date,
						"document_link": self.name
					})
					emp.save()
			