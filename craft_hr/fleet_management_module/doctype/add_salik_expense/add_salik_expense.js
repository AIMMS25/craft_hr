// Copyright (c) 2024, craft@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Add Salik Expense', {
    refresh: function(frm) {
        frm.add_custom_button(__('Create Salik Expense'), function() {
            frappe.confirm(__('Create and submit Salik Expenses for all entries?'), function() {
                frappe.call({
                    method: 'craft_hr.fleet_management_module.doctype.add_salik_expense.add_salik_expense.create_salik_expenses',
                    args: { trip_details: frm.doc.trip_details },
                    callback: function(response) {
                        if (response.message) {
                            frappe.show_alert({
                                message: __('Successfully created Salik Expenses for all entries.'),
                                indicator: 'green'
                            });
                            frm.clear_table('trip_details');
                            frm.refresh_field('trip_details');
                            frm.submit();
                        }
                    }
                });
            });
        });
    },
    onload: function(frm) {
        frm.disable_save();
    }
});


