// Copyright (c) 2024, Craftinteractive and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Missed Punch Report"] = {
    "filters": [
        {
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1
        }
    ],

    onload: function(report) {
        report.page.add_inner_button(__('Notify Users by Email'), function() {
            frappe.call({
                method: "craft_hr.craft_hr.report.missed_punch_report.missed_punch_report.send_report_emails",
                args: {
                    report_name: "Missed Punch Report",
                    filters: report.get_values() 
                },
                callback: function(response) {
                    if (response.message === 'success') {
                        frappe.msgprint(__('Email sent successfully.'));
                    } else {
                        frappe.msgprint(__('Failed to send email.'));
                    }
                },
                error: function() {
                    frappe.msgprint(__('An error occurred while sending emails.'));
                }
            });
        });
    }
};

