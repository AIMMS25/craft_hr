# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ConfinedSpaceEntryPermit(Document):
	pass

@frappe.whitelist()
def get_questions(template_name):
    template = frappe.get_doc('Atmosphere Reading Template', template_name)
    return template.reading_table
