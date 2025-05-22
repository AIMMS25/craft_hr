import frappe
from frappe import _
from frappe.utils import getdate, nowdate
from hrms.hr.doctype.leave_application.leave_application import get_leaves_for_period
from hrms.hr.utils import set_employee_name, validate_active_employee
from hrms.hr.doctype.leave_encashment.leave_encashment import LeaveEncashment


class CustomLeaveEncashment(LeaveEncashment):
    def validate(self):
        set_employee_name(self)
        validate_active_employee(self.employee)
        self.get_leave_details_for_encashment()
        self.validate_salary_structure()

        if not self.encashment_date:
            self.encashment_date = getdate(nowdate())

    @frappe.whitelist()
    def get_leave_details_for_encashment(self):
        salary_structure = get_second_last_salary_structure_assignment(
            self.employee, self.encashment_date or getdate(nowdate())
        )

        if not salary_structure:
            salary_structure = get_latest_salary_structure_assignment(self.employee)

        if not frappe.db.get_value("Leave Type", self.leave_type, "allow_encashment"):
            frappe.throw(_("Leave Type {0} is not encashable").format(self.leave_type))

        allocation = self.get_leave_allocation()

        if not allocation:
            frappe.throw(
                _("No Leaves Allocated to Employee: {0} for Leave Type: {1}").format(
                    self.employee, self.leave_type
                )
            )

        self.leave_balance = (
            allocation.total_leaves_allocated
            - allocation.carry_forwarded_leaves_count
            + get_leaves_for_period(
                self.employee, self.leave_type, allocation.from_date, self.encashment_date
            )
        )
        encashable_days = self.leave_balance - frappe.db.get_value(
            "Leave Type", self.leave_type, "encashment_threshold_days"
        )
        if not self.encashable_days:
            self.encashable_days = encashable_days if encashable_days > 0 else 0

        per_day_encashment = frappe.db.get_value(
            "Salary Structure Assignment", salary_structure, "custom_leave_encashment_amount_per_day"
        )
        self.encashment_amount = self.encashable_days * per_day_encashment if per_day_encashment > 0 else 0

        self.leave_allocation = allocation.name
        return True

def get_second_last_salary_structure_assignment(employee, on_date):
    if not employee or not on_date:
        return None
    salary_structure_assignments = frappe.db.sql(
        """
        SELECT name FROM `tabSalary Structure Assignment`
        WHERE employee=%(employee)s
        AND docstatus = 1
        AND %(on_date)s >= from_date 
        ORDER BY from_date DESC LIMIT 2""",
        {
            "employee": employee,
            "on_date": on_date,
        },
    )
    return salary_structure_assignments[1][0] if len(salary_structure_assignments) == 2 else None

def get_latest_salary_structure_assignment(employee):
    if not employee:
        return None
    salary_structure_assignment = frappe.db.sql(
        """
        SELECT name FROM `tabSalary Structure Assignment`
        WHERE employee=%(employee)s
        AND docstatus = 1
        ORDER BY from_date DESC LIMIT 1""",
        {"employee": employee},
    )
    return salary_structure_assignment[0][0] if salary_structure_assignment else None