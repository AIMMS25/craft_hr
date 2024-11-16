frappe.ui.form.on('Ticket Application', {
    employee: function(frm) {
        const employee = frm.doc.employee;

        frappe.db.get_value('Ticket Allocation', {
            employee: employee,
            docstatus: 1,
        }, ['earned_days', 'rounded_ticket_value_earned', 'eligibility', 'eligibility_date', 'name'], (values) => {
            if (values.name) {
                frm.set_value('eligibility', values.eligibility);

                if (values.eligibility === 'Eligible') {
                    frm.set_value('available_days', values.earned_days);
                    frm.set_value('rounded_ticket_value_earned', values.rounded_ticket_value_earned);
                } else if (frappe.datetime.get_diff(values.eligibility_date, frappe.datetime.nowdate()) > 0) {
                    let formatted_date = frappe.datetime.str_to_user(values.eligibility_date);
                    frappe.throw({
                        title: __('Ticket Application'),
                        message: __("You will be eligible for the Ticket Application only on {0}", [formatted_date])
                    });
                } else {
                    frm.set_value('available_days', null);
                    frm.set_value('rounded_ticket_value_earned', null);
                    frappe.msgprint(__('Employee is not eligible for ticket application.'));
                }
            } else {
                frappe.msgprint(__('No ticket has been allocated for this employee.'));
                frm.set_value('available_days', null);
                frm.set_value('rounded_ticket_value_earned', null);
                frm.set_value('eligibility', null);
            }
        });
    }
});
