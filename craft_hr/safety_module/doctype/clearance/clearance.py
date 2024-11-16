# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Clearance(Document):
	pass

@frappe.whitelist()
def get_site_pass_details(employee):
    site_passes = frappe.get_all("Site Pass", 
        filters={"employee": employee},
        fields=["name", "status"]
    )
    return site_passes
