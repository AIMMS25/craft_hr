# Copyright (c) 2024, Craftinteractive and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days, nowdate


class TicketApplication(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = frappe.get_single("Craft HR Settings")
        
        
    def validate(self, method=None):
       
        try:
            ticket_price = float(self.redeemed_ticket_price)
        except ValueError:
            frappe.throw("Invalid ticket price value", title="Invalid Data")

        if ticket_price > self.settings.threshold_amount:
            frappe.throw(
                f"The maximum ticket price is {self.settings.threshold_amount}",
                title="Ticket Price Exceeds Limit"
            )
        
        if ticket_price <= 0:
            frappe.throw(
                "The minimum ticket value should be greater than 0",
                title="Invalid Ticket Price"
            )

                
    def on_submit(self):
        used_days = self.settings.threshold_no_of_days

        ticket_allocation = frappe.get_doc("Ticket Allocation",{"employee":self.employee})
        ticket_allocation.used_days += used_days

        ticket_allocation.earned_days =  ticket_allocation.earned_days - used_days
        ticket_allocation.last_ticket_date = self.posting_date
        ticket_allocation.save()
        ticket_allocation.submit()


        additional_salary = frappe.new_doc("Additional Salary")
        additional_salary.employee = self.employee
        additional_salary.payroll_date = self.posting_date
        additional_salary.salary_component = "Ticket Reimbursement"
        additional_salary.amount = self.redeemed_ticket_price
        additional_salary.overwrite_salary_structure_amount = 1
        additional_salary.ticket_application = self.name
        additional_salary.insert()
        additional_salary.submit()


    def before_cancel(self):
        query = f"""
            SELECT
                ta.name AS name
            FROM
                `tabTicket Application` ta
            WHERE
                ta.employee = '{self.employee}' and docstatus =1
            ORDER BY
                ta.posting_date DESC
            LIMIT 1
        """
        data = frappe.db.sql(query, as_dict=1)
        
        if data[0].name != self.name:
            frappe.throw("Cannot cancel this")

    def on_cancel(self):        
        used_days = self.settings.threshold_no_of_days
        ticket_allocation = frappe.get_doc("Ticket Allocation", {"employee": self.employee, "docstatus": 1})
        ticket_allocation.used_days = ticket_allocation.used_days - used_days

        query = f"""
            SELECT
                ta.name AS name, ta.posting_date as date
            FROM
                `tabTicket Application` ta
            WHERE
                ta.employee = '{self.employee}' AND ta.docstatus = 1
            ORDER BY
                ta.posting_date DESC
            LIMIT 1
        """
        data = frappe.db.sql(query, as_dict=1)
        if data:
            ticket_allocation.last_ticket_date = data[0].date
        else:
            ticket_allocation.last_ticket_date = ""

        difference = ticket_allocation.used_days - ticket_allocation.earned_days

        if data:  # Check if there is a ticket application
            target_date = add_days(nowdate(), difference)
            ticket_allocation.db_set("eligibility_date", target_date)
        else:
            ticket_allocation.db_set("eligibility_date", None)  # Set eligibility_date to NULL

        ticket_allocation.save()
        ticket_allocation.submit()


