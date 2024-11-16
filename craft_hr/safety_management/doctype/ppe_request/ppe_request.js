frappe.ui.form.on('PPE Request', {
    onload: function(frm) {
        setTimeout(() => {
            $("button.btn-new[data-doctype='PPE Authorization']").hide();
        }, 10);

        frm.set_query('source_warehouse', function() {
            return {
                filters: {
                    company: frm.doc.company,
                    is_group: 0
                }
            };
        });

        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            const child = locals[cdt][cdn];
            if (frm.doc.source_warehouse) {
                return {
                    filters: {
                        is_stock_item: 1,
                        default_warehouse: frm.doc.source_warehouse
                    }
                };
            } else {
                return {
                    filters: {
                        is_stock_item: 1
                    }
                };
            }
        };
    }
});
