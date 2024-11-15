// Copyright (c) 2024, craft@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Pass', {
    date: function(frm) {
        calculate_remaining_days(frm);
    },
    site_pass_expiry: function(frm) {
        calculate_remaining_days(frm);
    }
});

function calculate_remaining_days(frm) {
    if (frm.doc.date && frm.doc.site_pass_expiry) {
        let date = new Date(frm.doc.date);
        let site_pass_expiry = new Date(frm.doc.site_pass_expiry);
        
        let timeDiff = site_pass_expiry - date;
        let remaining_days = Math.ceil(timeDiff / (1000 * 3600 * 24));

        frm.set_value('remaining_days', remaining_days);
    } else {
        frm.set_value('remaining_days', 0);
    }
}
