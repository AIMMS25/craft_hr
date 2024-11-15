// Copyright (c) 2024, Craft Interactive and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bed", {
    building_name: function(frm){
        if(!frm.doc.building_name){
            frm.set_value("floor_no","")
            frm.set_value("room_no","")
        }
    },
	refresh(frm) {

        frm.set_query("floor_no", function() {
            return {
                filters: {
                    building_name : frm.doc.building_name 
                }
            }
        });

        frm.set_query("room_no", function() {
            return {
                filters: {
                    floor_no: frm.doc.floor_no 
                }
            }
        });
	},
});
