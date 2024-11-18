

frappe.ui.form.on('Leave Application', {
    to_date: function(frm) {
        validate_and_set_prorated_leave(frm);
    },
    custom_leave: function(frm) {
        validate_and_set_prorated_leave(frm);
    },
    from_date: function(frm) {
        validate_and_set_prorated_leave(frm);
    }
});

function validate_and_set_prorated_leave(frm) {
    if (!frm.doc.employee || !frm.doc.leave_type || !frm.doc.from_date) {
        return;
    }

    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Leave Type",
            name: frm.doc.leave_type
        },
        callback: function(leave_type_res) {
            if (leave_type_res.message && leave_type_res.message.is_earned_leave) {
                if (leave_type_res.message.earned_leave_frequency === "Monthly") {
                    frappe.call({
                        method: "frappe.client.get_value",
                        args: {
                            doctype: "Leave Policy Assignment",
                            filters: { employee: frm.doc.employee },
                            fieldname: "leave_policy"
                        },
                        callback: function(res) {
                            if (res.message && res.message.leave_policy) {
                                frappe.call({
                                    method: "frappe.client.get",
                                    args: {
                                        doctype: "Leave Policy",
                                        name: res.message.leave_policy
                                    },
                                    callback: function(r) {
                                        if (r.message) {
                                            let leave_policy_details = r.message.leave_policy_details;
                                            let annual_allocation = 0;

                                            // Find the annual allocation for the specific leave type
                                            leave_policy_details.forEach(function(detail) {
                                                if (detail.leave_type === frm.doc.leave_type) {
                                                    annual_allocation = detail.annual_allocation;
                                                }
                                            });

                                            if (annual_allocation) {
                                                let to_date = new Date(frm.doc.to_date);
                                                let today = new Date();

                                                let total_months = ((to_date.getFullYear() - today.getFullYear()) * 12) + to_date.getMonth() - today.getMonth();
                                                let additional_leave = (annual_allocation / 12) * total_months;

                                                frm.set_value('custom_leave', additional_leave);

                                                frappe.call({
                                                    method: "hrms.hr.doctype.leave_application.leave_application.get_leave_balance_on",
                                                    args: {
                                                        employee: frm.doc.employee,
                                                        date: frm.doc.from_date,
                                                        to_date: frm.doc.to_date,
                                                        leave_type: frm.doc.leave_type,
                                                        consider_all_leaves_in_the_allocation_period: 1,
                                                    },
                                                    callback: function (r) {
                                                        if (!r.exc && r.message) {
                                                            let eligible_leave = r.message + additional_leave;
                                                            frm.set_value('leave_balance', eligible_leave);
                                                        }
                                                    }
                                                });
                                            }
                                        }
                                    }
                                });
                            }
                        }
                    });
                }
            }
        }
    });
}