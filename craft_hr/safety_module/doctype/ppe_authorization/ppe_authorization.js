// Copyright (c) 2024, craft@gmail.com and contributors
// For license information, please see license.txt



frappe.ui.form.on('PPE Authorization', {
    onload(frm) {
        setTimeout(()=>{
            $("button.btn-new[data-doctype='Stock Entry']").hide();
        },10);
    }
})

frappe.ui.form.on('PPE Authorization', {
    onload(frm) {
        setTimeout(()=>{
            $("button.btn-new[data-doctype='Expense Claim']").hide();
        },10);
    }
})
