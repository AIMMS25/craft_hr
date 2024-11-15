// Copyright (c) 2024, Craft Interactive and contributors
// For license information, please see license.txt


frappe.ui.form.on("Accommodation Transfer Form", {
    refresh: function(frm) {
        frm.set_query("to_floor_no", function() {
            return {
                filters: {
                    building_name: frm.doc.to_building_name
                }
            }
        });
        frm.set_query("to_room_no", function() {
            return {
                filters: {
                    floor_no: frm.doc.to_floor_no
                }
            }
        });

        frm.set_query("to_bed_no", function() {
            return {
                filters: {
                    room_no: frm.doc.to_room_no
                }
            }
        });
    },
        

//     employee(frm) {
//         if (frm.doc.employee) {
//             update_allocations(frm,true)
//             // frappe.call({
//             //     method: 'delight.delight.doctype.accommodation_transfer_form.accommodation_transfer_form.get_bed_details',
//             //     args: {
//             //         employee: frm.doc.employee
//             //     },
//             //     callback: function(r) {
//             //         if (r.message) {
//             //             let bed_info = `
//             //             <h5>This Employee Already Allocated in:</h5>
//             //             <table>
//             //                 <tr>
//             //                     <td><strong>Building</strong></td>
//             //                     <td>: ${r.message.building_name}</td>
//             //                 </tr>
//             //                 <tr>
//             //                     <td><strong>Floor</strong></td>
//             //                     <td>: ${r.message.floor_no}</td>
//             //                 </tr>
//             //                 <tr>
//             //                     <td><strong>Room Number</strong></td>
//             //                     <td>: ${r.message.room_no}</td>
//             //                 </tr>
//             //                 <tr>
//             //                     <td><strong>Bed Number</strong></td>
//             //                     <td>: ${r.message.bed_no}</td>
//             //                 </tr>
//             //             </table>
//             //         `;
//             //             frm.set_df_property('accommodation_info', 'options', bed_info);
//             //             frm.save();
//             //         } else {
//             //             frm.set_df_property('accommodation_info', 'options', '<p>No bed allocated to this employee.</p>');
//             //         }
//             //     }
//             // });
//         } else {
//             frm.set_df_property('accommodation_info', 'options', '');
//         }
//     },
//     accommodation_type(frm) {
//         // if (frm.doc.employee) {
//         // update_allocations(frm,false)
//         // }else{
//         //     frm.set_df_property('accommodation_info', 'options', '');
//         // }
//         if (frm.doc.accommodation_type == "Allocation"){
//             frm.set_value("from_building_name", '')
//             frm.set_value("from_floor_no", '')
//             frm.set_value("from_room_no", '')
//             frm.set_value("from_bed_no", '')
//         }
//     },


//     exit_employee(frm) {
//         frappe.confirm(
//             'Are you sure you want to exit the employee and vacate the bed?',
//             function() {
//                 frappe.call({
//                     method: 'delight.delight.doctype.accommodation_transfer_form.accommodation_transfer_form.exit_employee',
//                     args: {
//                         employee: frm.doc.employee,
//                         docname: frm.doc.name
//                     },
//                     callback: function(r) {
//                         if (r.message === 'success') {
//                             frm.clear_table('allocations'); // Clear current allocations
//                             frm.refresh_field('allocations'); // Refresh the allocations table
//                             frappe.msgprint(__('Employee exited and bed status updated to vacant.'));
//                         } else {
//                             frappe.msgprint(__('No bed found for this employee.'));
//                         }
//                     }
//                 });
//             }
//         );
//     },

//     transfer_employee(frm) {
//         if (frm.doc.employee) {
//             frappe.prompt([
//                 {
//                     label: 'Select New Bed',
//                     fieldname: 'new_bed',
//                     fieldtype: 'Link',
//                     options: 'Bed',
//                     reqd: 1,
//                     get_query: function() {
//                         return {
//                             filters: {
//                                 status: 'Vacant'
//                             }
//                         };
//                     }
//                 }
//             ], function(values){
//                 frappe.call({
//                     method: 'delight.delight.doctype.accommodation_transfer_form.accommodation_transfer_form.transfer_employee_bed',
//                     args: {
//                         employee: frm.doc.employee,
//                         new_bed: values.new_bed,
//                         docname: frm.doc.name
//                     },
//                     callback: function(r) {
//                         if (r.message === 'success') {
//                             frm.clear_table('allocations'); // Clear current allocations
//                             frm.refresh_field('allocations'); // Refresh the allocations table
//                             frappe.msgprint(__('Employee has been successfully transferred to the new bed.'));
//                         } else {
//                             frappe.msgprint(__('An error occurred during the transfer process.'));
//                         }
//                     }
//                 });
//             }, 'Transfer Employee to New Bed', 'Transfer');
//         } else {
//             frappe.msgprint(__('Please select an employee first.'));
//         }
//     },
});


// // function update_allocations(frm, save_form){
// //     // if (frm.doc.employee) {
// //         frappe.call({
// //             method: 'delight.delight.doctype.accommodation_transfer_form.accommodation_transfer_form.get_bed_details',
// //             args: {
// //                 employee: frm.doc.employee
// //             },
// //             callback: function(r) {
// //                 if (r.message) {
// //                 //     let bed_info = `
// //                 //     <h5>This Employee Already Allocated in:</h5>
// //                 //     <table>
// //                 //         <tr>
// //                 //             <td><strong>Building</strong></td>
// //                 //             <td>: ${r.message.building_name}</td>
// //                 //         </tr>
// //                 //         <tr>
// //                 //             <td><strong>Floor</strong></td>
// //                 //             <td>: ${r.message.floor_no}</td>
// //                 //         </tr>
// //                 //         <tr>
// //                 //             <td><strong>Room Number</strong></td>
// //                 //             <td>: ${r.message.room_no}</td>
// //                 //         </tr>
// //                 //         <tr>
// //                 //             <td><strong>Bed Number</strong></td>
// //                 //             <td>: ${r.message.bed_no}</td>
// //                 //         </tr>
// //                 //     </table>
// //                 // `;
// //                 //     frm.set_df_property('accommodation_info', 'options', bed_info);
// //                 frm.set_value("from_floor_no", r.message.floor_no)
// //                     if(save_form){
// //                         frm.save();
// //                     }
                    
// //                 } else {
// //                     frm.set_df_property('accommodation_info', 'options', '<p>No bed allocated to this employee.</p>');
// //                 }
// //             }
// //         });
//     // } else {
//     //     frm.set_df_property('accommodation_info', 'options', '');
//     // }
// // }