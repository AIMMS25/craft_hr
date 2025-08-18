frappe.query_reports["IRATA Certificate Expiry"] = {
    filters: [
        {
            fieldname: "expiry_range",
            label: "Expiring In (Days)",
            fieldtype: "Select",
            options: ["30", "60", "90"],
            default: "60"
        }
    ]
};