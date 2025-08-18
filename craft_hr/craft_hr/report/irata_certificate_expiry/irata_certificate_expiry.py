import frappe
from frappe.utils import today

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Employee ID", "fieldname": "employee_number", "fieldtype": "Data", "width": 100},
        {"label": "Employee Name", "fieldname": "first_name", "fieldtype": "Data", "width": 150},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 120},
        {"label": "Cert. Type", "fieldname": "cert_type", "fieldtype": "Data", "width": 80},
        {"label": "Doc No.", "fieldname": "custom_irata_no", "fieldtype": "Data", "width": 100},
        {"label": "Expiry Date", "fieldname": "custom_irata_validity", "fieldtype": "Date", "width": 120},
        {"label": "Expiry in Days", "fieldname": "expiry_in_days", "fieldtype": "Int", "width": 120},
    ]

def get_data(filters):
    expiry_limit = int(filters.get("expiry_range") or 60)

    return frappe.db.sql("""
        SELECT 
            emp.employee_number,
            emp.first_name,
            emp.designation,
            'IRATA' AS cert_type,
            emp.custom_irata_no,
            emp.custom_irata_validity,
            DATEDIFF(emp.custom_irata_validity, CURDATE()) AS expiry_in_days
        FROM 
            `tabEmployee` emp
        WHERE 
            emp.status = 'Active'
            AND DATEDIFF(emp.custom_irata_validity, CURDATE()) BETWEEN 0 AND %(expiry_limit)s
        GROUP BY  
            emp.employee_number, emp.first_name, emp.designation, emp.custom_irata_no, emp.custom_irata_validity
        ORDER BY 
            expiry_in_days ASC
    """, {"expiry_limit": expiry_limit}, as_dict=True)
