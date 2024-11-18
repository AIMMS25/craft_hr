


import frappe

def on_submit(doc, method):
    ss = frappe.db.get_value("Employee", doc.employee, "custom_salary_structure")

    if ss:
        ssa = frappe.get_doc(
            {   
                "doctype": "Salary Structure Assignment",
                "employee": doc.employee,
                "salary_structure": ss,
                "from_date": doc.promotion_date,
                "sc_basic": doc.custom_new_basic,
                "sc_hra": doc.custom_new_hra,
                "sc_transport": doc.custom_new_transport_allowance,
                "sc_cola": doc.custom_new_other_allowance,
            }
        )

        ssa.save(ignore_permissions=True)
        ssa.submit()
        frappe.msgprint("Salary Structure Assignment created successfully.")
    else:
        frappe.msgprint("No Salary Structure found for the given employee.")

def before_validate(doc, method):
    existing_total = (
        (doc.custom_basic or 0) +
        (doc.custom_hra or 0) +
        (doc.custom_transport_allowance or 0) +
        (doc.custom_other_allowance or 0)
    )
    doc.custom_existing_total = existing_total

    new_total = (
        (doc.custom_new_basic or 0) +
        (doc.custom_new_hra or 0) +
        (doc.custom_new_transport_allowance or 0) +
        (doc.custom_new_other_allowance or 0)
    )
    doc.custom_new_total = new_total

