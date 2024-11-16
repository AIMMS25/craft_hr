
# Copyright (c) 2024, Craft Interactive and contributors
# For license information, please see license.txt

import frappe

def get_columns():
    columns = [
        {
            "label": "Employee ID",
            "fieldname": "employee_id",
            "fieldtype": "Data",
            "width": 400
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 400
        },
        {
            "label": "User ID",
            "fieldname": "user_id",
            "fieldtype": "Data",
            "width": 450
        }
    ]
    return columns

def get_data(filters):
    date = filters.get("date")

    data = frappe.db.sql("""
        SELECT 
            emp.name AS employee_id, 
            emp.employee_name, 
            emp.user_id
        FROM 
            `tabEmployee` emp
        LEFT JOIN 
            `tabAttendance` att ON emp.name = att.employee
            AND att.attendance_date = %(date)s
        LEFT JOIN 
            `tabEmployee Checkin` chk ON emp.name = chk.employee
            AND DATE(chk.time) = %(date)s
        WHERE 
            att.name IS NULL
            AND chk.name IS NULL
        ORDER BY 
            emp.employee_name
    """, {"date": date}, as_dict=1)

    return data

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


@frappe.whitelist()
def send_report_emails(report_name):
    report_data = frappe.db.sql("""
        SELECT emp.user_id
        FROM `tabEmployee` emp
        LEFT JOIN `tabAttendance` att ON emp.name = att.employee
        WHERE att.attendance_date IS NULL
    """, as_dict=1)

    recipients = [row.get("user_id") for row in report_data if row.get("user_id")]

    if recipients:
        message = """
            <h2>Missed Punch Report</h2>
            <p>Please find the attached missed punch report.</p>
        """

        frappe.sendmail(
            recipients=recipients,
            subject="Missed Punch Report",
            message=message,
            now=True  
        )

        frappe.msgprint("Emails sent successfully to the users.")
    else:
        frappe.msgprint("No email addresses found in the report.")



