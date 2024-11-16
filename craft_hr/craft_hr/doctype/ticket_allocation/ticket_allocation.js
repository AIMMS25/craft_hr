// Copyright (c) 2024, Craftinteractive and contributors
// For license information, please see license.txt



frappe.ui.form.on('Ticket Allocation', {
    refresh: function(frm) {
        if (frm.doc.docstatus == 1 && frm.doc.eligibility == 'Eligible') {
            frm.add_custom_button(__('Ticket Application'), function() {
            frappe.model.open_mapped_doc({
                method: "craft_hr.craft_hr.doctype.ticket_allocation.ticket_allocation.ticket_application",
                frm: frm
            })
            }, __('Create'));
        }
    }
});
