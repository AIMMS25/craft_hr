// Copyright (c) 2024, craft@gmail.com and contributors
// For license information, please see license.txt



frappe.ui.form.on('Clearance', {
    employee: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: "craft_hr.safety_module.doctype.clearance.clearance.get_site_pass_details",
                args: {
                    employee: frm.doc.employee
                },
                callback: function(r) {
                    frm.clear_table("site_pass_details");

                    if (r.message && r.message.length > 0) {
                        $.each(r.message, function(i, d) {
                            var row = frm.add_child("site_pass_details");
                            row.site_pass_name = d.name;
                            row.status = d.status;
                        });
                    }
                    frm.refresh_field("site_pass_details");
                }
            });
        } else {
            frm.clear_table("site_pass_details");
            frm.refresh_field("site_pass_details");
        }
    }
});

