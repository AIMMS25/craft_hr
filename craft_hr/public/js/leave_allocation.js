frappe.ui.form.on("Leave Allocation",{
    refresh: function(frm){
        frappe.db.get_single_value("Craft HR Settings", "leave_allocation_based_on_leave_distribution_template").then((value) => {
            frm.toggle_display("custom_is_earned_leave", value)
            if(frm.doc.docstatus != 1 && frm.doc.custom_is_earned_leave && !value){
                frm.set_value("custom_is_earned_leave",0)
            }
        });
    },
    onload: function(frm){
        if(frm.doc.custom_status=="Ongoing" && frm.doc.docstatus){
            frm.add_custom_button(__('Close'), function(){
                if(frm.doc.from_date<frappe.datetime.get_today()){
                    frappe.confirm(__("Are you sure you want to close this allocation?"), function(){
                        frappe.call({
                            method:"craft_hr.events.leave_allocation.close_allocation",
                            args:{
                                docname : frm.doc.name
                            },
                            callback: function(r){
                                console.log("Success")
                            }
                        })
                    })
                }
                else {
                    frappe.msgprint(__("This leave allocation period has not started yet."))
                }
            })
        }
    }
})