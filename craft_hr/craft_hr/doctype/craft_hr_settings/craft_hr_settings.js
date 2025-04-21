// Copyright (c) 2023, Craftinteractive and contributors
// For license information, please see license.txt

frappe.ui.form.on('Craft HR Settings', {
	threshold_amount: function(frm) {
        const thresholdAmount = frm.doc.threshold_amount;
        const thresholdNoDays = frm.doc.threshold_no_of_days;

        const perDayAmount = thresholdAmount / thresholdNoDays;

        frm.set_value('per_day_amount', perDayAmount);
    },
    threshold_no_of_days: function(frm) {
        const thresholdAmount = frm.doc.threshold_amount;
        const thresholdNoDays = frm.doc.threshold_no_of_days;
        const perDayAmount = thresholdAmount / thresholdNoDays;
        frm.set_value('per_day_amount', perDayAmount);
    }
});