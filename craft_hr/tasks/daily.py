import frappe
from craft_hr.events.get_leaves import get_earned_leave

def reset_leave_allocation():
    filters = {
        "reset_allocation_on_expiry": 1,
        "to_date": ["<=", frappe.utils.getdate()],
        "docstatus": 1,
        "custom_status": "Ongoing"
    }
    allocations = frappe.db.get_all("Leave Allocation", filters=filters, pluck="name")
    for allocation_name in allocations:
        allocation = frappe.get_doc("Leave Allocation", allocation_name)
        new_allocation = frappe.copy_doc(allocation)
        new_allocation.from_date = frappe.utils.add_days(new_allocation.to_date, 1)
        new_allocation.to_date = frappe.utils.add_years(new_allocation.to_date, 1)
        carry_forward = frappe.db.get_single_value("Craft HR Settings", "reset_allocation_with_carry_forward") or 0
        new_allocation.carry_forward = carry_forward
        new_allocation.new_leaves_allocated = new_allocation.reset_to
        new_allocation.insert(ignore_permissions=True)
        if carry_forward:
            new_allocation.update({
                "custom_opening_leaves": new_allocation.unused_leaves,
            })
        new_allocation.save()
        new_allocation.submit()
        allocation.db_set("custom_status", "Closed")

def update_leave_allocations():
    get_earned_leave()
