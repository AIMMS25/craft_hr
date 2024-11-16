frappe.ui.form.on('Expenses', {
    refresh: function(frm) {
        frm.add_custom_button(__('Create Vehicle Log'), function() {
            if (frm.doc.expense_type === 'Fuel') {
                frappe.confirm(__('Create and submit Vehicle Logs for all Fuel entries?'), function() {
                    frappe.call({
                        method: 'craft_hr.fleetmanagement_module.doctype.expenses.expenses.create_fuel_vehicle_logs',
                        args: { fuel_expense: frm.doc.fuel_expense },
                        callback: function(response) {
                            if (response.message) {
                                frappe.show_alert({
                                    message: __('Successfully created Vehicle Log for all fuel entries.'),
                                    indicator: 'green'
                                });
                                frm.clear_table('fuel_expense');
                                frm.refresh_field('fuel_expense');
                                frm.save();
                            }
                        }
                    });
                });
            } else if (frm.doc.expense_type === 'Service') {
                frappe.confirm(__('Create and submit Vehicle Logs for all Service entries?'), function() {
                    frappe.call({
                        method: 'craft_hr.fleetmanagement_module.doctype.expenses.expenses.create_service_vehicle_logs',
                        args: { service_expense: frm.doc.service_expense },
                        callback: function(response) {
                            if (response.message) {
                                frappe.show_alert({
                                    message: __('Successfully created Vehicle Logs for all service entries.'),
                                    indicator: 'green'
                                });
                                frm.clear_table('service_expense');
                                frm.refresh_field('service_expense');
                                frm.save();
                            }
                        }
                    });
                });
            } else {
                frappe.msgprint(__('No entries found or Expense Type is not valid.'));
            }
        });
        frm.disable_save();

    },
    onload: function(frm) {
        frm.disable_save();
    }
});
