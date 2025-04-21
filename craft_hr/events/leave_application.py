
import frappe
from craft_hr.events.get_leaves import get_earned_leave
from datetime import timedelta
from frappe.utils import getdate, flt


import datetime

from hrms.hr.doctype.leave_application.leave_application import get_leave_balance_on

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def days_in_year(year):
    return 366 if is_leap_year(year) else 365

def on_submit(doc, method):
    # TODO: condition to check if the leave type is earned leave
    get_earned_leave(doc.employee)

from datetime import datetime, timedelta

def validate(self, method):
    # leave_balance = get_leave_balance_on(
    #     employee=self.employee,
    #     date=self.from_date,
    #     to_date=self.to_date,
    #     leave_type=self.leave_type,
    #     consider_all_leaves_in_the_allocation_period=1
    # )

    # if leave_balance:
    #     leave_type_doc = frappe.get_doc("Leave Type", self.leave_type)
        
    #     if leave_type_doc.is_earned_leave and leave_type_doc.earned_leave_frequency == 'Monthly':
    #         leave_policy_assignment = frappe.get_value("Leave Policy Assignment", {"employee": self.employee}, "leave_policy")
            
    #         if leave_policy_assignment:
    #             leave_policy_doc = frappe.get_doc("Leave Policy", leave_policy_assignment)

    #             annual_allocation = None
    #             for detail in leave_policy_doc.leave_policy_details:
    #                 if detail.leave_type == self.leave_type:
    #                     annual_allocation = detail.annual_allocation
    #                     break

    #             if annual_allocation:
    #                 to_date = datetime.strptime(self.to_date, '%Y-%m-%d')
    #                 today = datetime.today()

    #                 total_months = (to_date.year - today.year) * 12 + to_date.month - today.month

    #                 additional_leave = (annual_allocation / 12) * total_months

    #                 self.custom_leave = additional_leave

    #                 eligible_leave = leave_balance + additional_leave

    #                 self.leave_balance = eligible_leave

    #                 if self.total_leave_days > eligible_leave:
    #                     frappe.msgprint(
    #                         _('Your total leave days exceed the eligible leave till {0}.').format(
    #                             frappe.utils.formatdate(self.to_date)
    #                         ),
    #                         title=_('Leave Balance Exceeded'),
    #                         indicator='orange'
    #                     )
    #         else:
    #             frappe.msgprint(
    #                 ('No leave policy assignment found for the employee.'),
    #                 title=('Leave Policy Error'),
    #                 indicator='red'
    #             )



    query = """
    SELECT 
        sa.salary_structure,
        sa.sc_basic,
        sa.sc_hra,
        sa.leave_salary,
        sa.from_date,
        COALESCE(
            (SELECT MIN(next_sa.from_date) 
             FROM `tabSalary Structure Assignment` next_sa 
             WHERE next_sa.employee = sa.employee 
               AND next_sa.from_date > sa.from_date AND next_sa.docstatus = 1),
            %(to_date)s
        ) AS to_date
    FROM 
        `tabSalary Structure Assignment` sa
    WHERE 
        sa.employee = %(employee)s
        AND sa.from_date <= %(to_date)s
        AND sa.from_date IS NOT NULL
        AND sa.docstatus = 1
    """

    if frappe.get_value("Leave Type",self.leave_type,"calculate_leave_salary") == 1:
        salary_structures = frappe.db.sql(query, {
            'employee': self.employee,
            'from_date': self.from_date,
            'to_date': self.to_date
        }, as_dict=True)
        total_prorated_base = 0

        for structure in salary_structures:
            # Calculate the effective date range
            effective_from_date = max(frappe.utils.getdate(structure.from_date), frappe.utils.getdate(self.from_date))
            effective_to_date = min(frappe.utils.getdate(structure.to_date), frappe.utils.getdate(self.to_date))
            
            # Calculate the number of active days within the range
            active_days = (effective_to_date - effective_from_date).days + 1
            if active_days > 0:
                leave_salary_percentage = structure.leave_salary / 100
                year_days = days_in_year(effective_from_date.year)
                proprated_base = ((((structure.sc_basic+structure.sc_hra)*12)*leave_salary_percentage)/year_days)*active_days
                total_prorated_base += proprated_base

        self.custom_leave_salary = total_prorated_base