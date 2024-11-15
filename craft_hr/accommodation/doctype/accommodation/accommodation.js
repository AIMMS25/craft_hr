// Copyright (c) 2024, Craft Interactive and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Accommodation', {
//     after_save: function(frm) {
//         console.log("Building Name Selected:", frm.doc.building_name);
//         if (frm.doc.building_name) {
//             frappe.call({
//                 method: "delight.delight.doctype.accommodation.accommodation.update_counts",
//                 args: {
//                     accommodation_name: frm.doc.name
//                 },
//                 callback: function(r) {
//                     console.log("Received Response:", r.message);
//                     if (r.message && r.message.building_name == frm.doc.building_name) {
//                         frm.set_value("floor", r.message.floor);
//                         frm.set_value("room", r.message.room);
//                         frm.set_value("bed", r.message.bed);
//                     }else{
//                         frm.set_value("floor", 0);
//                         frm.set_value("room", 0);
//                         frm.set_value("bed", 0);
//                     }
//                 }
//             });
//         } else {
//             frm.set_value("floor", 0);
//             frm.set_value("room", 0);
//             frm.set_value("bed", 0);
//         }
//     },
   
// });


frappe.ui.form.on('Accommodation', {
    after_save: function(frm) {
        console.log("Building Name Selected:", frm.doc.building_name);
        if (frm.doc.building_name) {
            frappe.call({
                method: "craft_hr.accommodation.doctype.accommodation.accommodation.update_counts",
                args: {
                    accommodation_name: frm.doc.name
                },
                callback: function(r) {
                    console.log("Received Response:", r.message);
                    if (r.message && r.message.building_name == frm.doc.building_name) {
                        let floorChanged = frm.doc.floor !== r.message.floor;
                        let roomChanged = frm.doc.room !== r.message.room;
                        let bedChanged = frm.doc.bed !== r.message.bed;

                        if (floorChanged || roomChanged || bedChanged) {
                            frm.set_value("floor", r.message.floor);
                            frm.set_value("room", r.message.room);
                            frm.set_value("bed", r.message.bed);

                            frm.save();
                        }
                    } else {
                        frm.set_value("floor", 0);
                        frm.set_value("room", 0);
                        frm.set_value("bed", 0);
                    }
                }
            });
        } else {
            frm.set_value("floor", 0);
            frm.set_value("room", 0);
            frm.set_value("bed", 0);
        }
    },
});
