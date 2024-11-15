// Copyright (c) 2024, craft@gmail.com and contributors
// For license information, please see license.txt



frappe.ui.form.on('Confined Space Entry Permit', {
    atmosphere_reading_template: function(frm) {
        if (frm.doc.atmosphere_reading_template) {
            frappe.call({
                method: "craft_hr.safety_module.doctype.confined_space_entry_permit.confined_space_entry_permit.get_questions",
                args: {
                    "template_name": frm.doc.atmosphere_reading_template
                },
                callback: function(r) {
                    if (r.message) {
                        frm.clear_table('reading_table');
                        $.each(r.message, function(i, d) {
                            var row = frm.add_child('reading_table');
                            row.atmosphere = d.atmosphere;
                            row.range = d.range;
                        });
                        frm.refresh_field('reading_table');
                    }
                }
            });
        } else {
            frm.clear_table('reading_table');
            frm.refresh_field('reading_table');
        }
    }
});




