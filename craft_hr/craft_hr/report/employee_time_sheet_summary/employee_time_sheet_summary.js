// Copyright (c) 2024, Craftinteractive and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Time Sheet Summary"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		{
            "fieldname": "from_date",
            "label": __("From date"),
            "fieldtype": "Date",
        },
		{
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
        },
		{
            "fieldname": "summarized_view",
            "label": __("Summarized View"),
            "fieldtype": "Check",
        },
	]
};