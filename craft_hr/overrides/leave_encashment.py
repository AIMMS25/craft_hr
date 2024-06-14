# # Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt


# import frappe
# from frappe import _
# from frappe.utils import format_date
# from hrms.hr.doctype.leave_encashment.leave_encashment import LeaveEncashment



# class CustomLeaveEncashment(LeaveEncashment):
#   # def validate(self):
#   #   set_employee_name(self)
#   #   validate_active_employee(self.employee)
#   #   self.encashment_date = self.encashment_date or getdate()
#   #   self.set_salary_structure_assignment()
#   #   self.get_leave_details_for_encashment()

#   # def before_save(self):
#   #   if self.encashment_days:
#   #     self.set_encashment_amount()


#   def set_salary_structure_assignment(self):
#     self._salary_structure_assignment = get_assigned_salary_structure_assignment(self.employee, self.encashment_date)
#     if not self._salary_structure_assignment:
#       frappe.throw(
#         _("No Salary Structure Assignment assigned to Employee {0} on the given date {1}").format(
#           self.employee, frappe.bold(format_date(self.encashment_date))
#         )
#       )

#   def set_encashment_amount(self):
#       if not hasattr(self, "_salary_structure_assignment"):
#         self.set_salary_structure_assignment()
#         per_day_encashment = frappe.db.get_value(
#           "Salary Structure Assignment", self._salary_structure_assignment, "custom_leave_encashment_amount_per_day"
#           )
#         self.encashment_amount = self.encashment_days * per_day_encashment if per_day_encashment > 0 else 0


# def get_assigned_salary_structure_assignment(employee, on_date):
#     if not employee or not on_date:
#         return None
#     salary_structure_assignment = frappe.db.sql(
#         """
#         select name from tabSalary Structure Assignment
#         where employee=%(employee)s
#         and docstatus = 1
#         and %(on_date)s >= from_date order by from_date desc limit 1""",
#         {
#             "employee": employee,
#             "on_date": on_date,
#             },
#             )
#     return salary_structure_assignment[0][0] if salary_structure_assignment else None