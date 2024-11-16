// Copyright (c) 2024, craft@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lifting Permit', {
    total_lifting_load: function(frm) {
        calculate_crane_utilization(frm);
    },
    capacity_of_crane: function(frm) {
        calculate_crane_utilization(frm);
    }
});

function calculate_crane_utilization(frm) {
    if (frm.doc.capacity_of_crane && frm.doc.capacity_of_crane != 0) {
        let utilization = (frm.doc.total_lifting_load / frm.doc.capacity_of_crane) * 100;
        frm.set_value('percentage_crane_utilization', utilization);
    }
}

