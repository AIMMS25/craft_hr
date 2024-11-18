

frappe.ui.form.on('Employee Promotion', {
    employee: function(frm) {
        frappe.db.get_list('Salary Structure Assignment', {
            filters: {
                'employee': frm.doc.employee,
                'docstatus': 1
            },
            fields: ['name', 'creation'],
            order_by: 'creation desc',
            limit: 1
        }).then(res => {
            if (res && res.length > 0) {
                frappe.db.get_doc('Salary Structure Assignment', res[0].name).then(r => {
                    frm.set_value('custom_basic', r.sc_basic);
                    frm.set_value('custom_hra', r.sc_hra);
                    frm.set_value('custom_transport_allowance', r.sc_transport);
                    frm.set_value('custom_other_allowance', r.sc_cola);
                });
            } else {
                frappe.msgprint('No Salary Structure Assignment found for this employee');
            }
        });
    }
});
