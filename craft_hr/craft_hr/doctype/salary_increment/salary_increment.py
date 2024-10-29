# Copyright (c) 2024, Craftinteractive and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalaryIncrement(Document):
	pass

@frappe.whitelist()
def latest_salary_structure(employee):
    salary_structure_assignment = frappe.db.sql("""
        SELECT name FROM `tabSalary Structure Assignment`
        WHERE employee = %s AND docstatus = 1
        ORDER BY creation DESC
        LIMIT 1
    """, (employee), as_dict=True)

    if salary_structure_assignment:
        ssa_doc = frappe.get_doc('Salary Structure Assignment', salary_structure_assignment[0].name)
        components = {
            "basic": ssa_doc.sc_basic,
            "hra": ssa_doc.sc_hra,
            "transport_allowance": ssa_doc.sc_transport,
            "cost_of_living_allowance" : ssa_doc.sc_cola,
            "other_allowance": ssa_doc.sc_other,
            "insurance_allowance" : ssa_doc.sc_insurance,
            "food_allowance" : ssa_doc.sc_food,
            "car_allowance" : ssa_doc.sc_car,
            "mobile_allowance" :ssa_doc.sc_mobile,
            "overtime_hourly_rate":ssa_doc.ot_rate,
            "fuel_allowance" :ssa_doc.sc_fuel,
            "leave_encashment_amount_per_day" :ssa_doc.custom_leave_encashment_amount_per_day,
            "job_well_done" :ssa_doc.sc_jwd,
            "position_level" :ssa_doc.sc_position_level,
            "attendance_bonus" :ssa_doc.sc_attendance_bonus,
            "holiday_overtime_rate" :ssa_doc.holiday_ot_rate
            
        }
        return components
    else:
        frappe.throw(f"No Salary Structure Assignment found for employee {employee}")

