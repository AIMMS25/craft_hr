// Copyright (c) 2024, Craftinteractive and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Salary Increment", {
// 	refresh(frm) {

// 	},
// });


// Copyright (c) 2024, Craftinteractive and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Increment', {
    employee: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: 'craft_hr.craft_hr.doctype.salary_increment.salary_increment.latest_salary_structure',
                args: {
                    employee: frm.doc.employee
                },
                callback: function(response) {
                    if (response.message) {
                        let components = response.message;

                        frm.clear_table('components');

                        let row = frm.add_child('components');
                        row.basic = components.basic;
                        row.hra = components.hra;
                        row.transport_allowance = components.transport_allowance;
                        row.cost_of_living_allowance = components.cost_of_living_allowance;
                        row.other_allowance = components.other_allowance;
                        row.insurance_allowance = components.insurance_allowance;
                        row.food_allowance = components.food_allowance;
                        row.car_allowance = components.car_allowance;
                        row.mobile_allowance = components.mobile_allowance;
                        row.overtime_hourly_rate = components.overtime_hourly_rate;
                        row.fuel_allowance = components.fuel_allowance;
                        row.leave_encashment_amount_per_day = components.leave_encashment_amount_per_day;
                        row.job_well_done = components.job_well_done;
                        row.position_level = components.position_level;
                        row.attendance_bonus = components.attendance_bonus;
                        row.holiday_overtime_rate = components.holiday_overtime_rate;

                        frm.refresh_field('components');
                    } else {
                        frm.clear_table('components');
                        frm.refresh_field('components');
                        frappe.msgprint(__('No salary structure assignment found for this employee.'));
                    }
                }
            });
        } else {
            frm.clear_table('components');
            frm.refresh_field('components');
        }
    },
    delete_component: function(frm) {
        if (!frm.doc.components || frm.doc.components.length === 0) {
            frappe.show_alert({
                message: __('No components to delete'),
                indicator: 'orange'
            });
            return;
        }
    
        const lastComponent = frm.doc.components[frm.doc.components.length - 1];
        
        if (!lastComponent.increment_date) {
            frappe.show_alert({
                message: __('The last component does not have an increment date.'),
                indicator: 'orange'
            });
            return;
        }
    
        frappe.db.get_value('Salary Structure Assignment', { 
            employee: frm.doc.employee, 
            from_date: lastComponent.increment_date 
        }, 'name', function (result) {
            if (result.name) {
                frappe.confirm(
                    __('Are you sure you want to delete the last row? This will also require you to delete the corresponding Salary Structure Assignment: {0}.', [result.name]),
                    function() {
                        frm.doc.components.pop();
                        frm.save();
                        frm.refresh_field('components');
                    }
                );
            } else {
                frappe.confirm(
                    __('Are you sure you want to delete the last row?'),
                    function() {
                        frm.doc.components.pop();
                        frm.save();
                        frm.refresh_field('components');
                    }
                );
            }
        });
    },
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Add Salary'), function() {
                const default_components = frm.doc.components[frm.doc.components.length - 1];

                let d = new frappe.ui.Dialog({
                    title: 'Add Salary Details',
                    fields: [
                        { fieldname: 'salary_increment', label: 'Salary Increment', fieldtype: 'Link', options: 'Salary Increment', default: frm.doc.name },
                        { fieldname: 'employee', label: 'Employee', fieldtype: 'Link', options: 'Employee', default: frm.doc.employee, read_only: 1 },
                        { fieldname: 'date', label: 'Date', fieldtype: 'Date', default: frm.doc.date },
                        { fieldname: 'salary_structure', label: 'Salary Structure', fieldtype: 'Link', options: 'Salary Structure' },
                        { fieldname: 'increment_amount', label: 'Increment Amount', fieldtype: 'Currency' },
                        { fieldname: 'basic', label: 'Basic', fieldtype: 'Currency', default: default_components.basic },
                        { fieldname: 'hra', label: 'HRA', fieldtype: 'Currency', default: default_components.hra },
                        { fieldname: 'transport_allowance', label: 'Transport Allowance', fieldtype: 'Currency', default: default_components.transport_allowance },
                        { fieldname: 'cost_of_living_allowance', label: 'Cost of Living Allowance', fieldtype: 'Currency', default: default_components.cost_of_living_allowance },
                        { fieldname: 'other_allowance', label: 'Other Allowance', fieldtype: 'Currency', default: default_components.other_allowance },
                        { fieldname: 'insurance_allowance', label: 'Insurance Allowance', fieldtype: 'Currency', default: default_components.insurance_allowance },
                        { fieldname: 'food_allowance', label: 'Food Allowance', fieldtype: 'Currency', default: default_components.food_allowance },
                        { fieldname: 'car_allowance', label: 'Car Allowance', fieldtype: 'Currency', default: default_components.car_allowance },
                        { fieldname: 'mobile_allowance', label: 'Mobile Allowance', fieldtype: 'Currency', default: default_components.mobile_allowance },
                        { fieldname: 'overtime_hourly_rate', label: 'Overtime Hourly Rate', fieldtype: 'Currency', default: default_components.overtime_hourly_rate },
                        { fieldname: 'fuel_allowance', label: 'Fuel Allowance', fieldtype: 'Currency', default: default_components.fuel_allowance },
                        { fieldname: 'leave_encashment_amount_per_day', label: 'Leave Encashment Amount Per Day', fieldtype: 'Currency', default: default_components.leave_encashment_amount_per_day },
                        { fieldname: 'job_well_done', label: 'Job Well Done', fieldtype: 'Currency', default: default_components.job_well_done },
                        { fieldname: 'position_level', label: 'Position Level', fieldtype: 'Currency', default: default_components.position_level },
                        { fieldname: 'attendance_bonus', label: 'Attendance Bonus', fieldtype: 'Currency', default: default_components.attendance_bonus },
                        { fieldname: 'holiday_overtime_rate', label: 'Holiday Overtime Rate', fieldtype: 'Currency', default: default_components.holiday_overtime_rate }
                    ],
                    primary_action_label: 'Save',
                    primary_action: function(data) {
                        frappe.confirm(
                            'Are you sure you want to submit?',
                            function() {
                                frappe.call({
                                    method: 'frappe.client.submit',
                                    args: {
                                        doc: {
                                            doctype: 'Salary Structure Assignment',
                                            employee: data.employee,
                                            custom_salary_increment: data.name,
                                            salary_structure: data.salary_structure,
                                            from_date: data.date,
                                            sc_basic: data.basic,
                                            sc_hra: data.hra,
                                            sc_transport: data.transport_allowance,
                                            sc_cola: data.cost_of_living_allowance,
                                            sc_other: data.other_allowance,
                                            sc_insurance: data.insurance_allowance,
                                            sc_food: data.food_allowance,
                                            sc_car: data.car_allowance,
                                            sc_mobile: data.mobile_allowance,
                                            ot_rate: data.overtime_hourly_rate,
                                            sc_fuel: data.fuel_allowance,
                                            custom_leave_encashment_amount_per_day: data.leave_encashment_amount_per_day,
                                            sc_jwd: data.job_well_done,
                                            sc_position_level: data.position_level,
                                            sc_attendance_bonus: data.attendance_bonus,
                                            holiday_ot_rate: data.holiday_overtime_rate,
                                            custom_salary_increment: data.salary_increment
                                        }
                                    },
                                    callback: function(response) {
                                        if (response.message) {
                                            frappe.show_alert({
                                                message: __('Salary Structure Assignment created successfully'),
                                                indicator: 'green'
                                            });

                                            let row = frm.add_child('components');
                                            row.basic = data.basic;
                                            row.hra = data.hra;
                                            row.transport_allowance = data.transport_allowance;
                                            row.cost_of_living_allowance = data.cost_of_living_allowance;
                                            row.other_allowance = data.other_allowance;
                                            row.insurance_allowance = data.insurance_allowance;
                                            row.food_allowance = data.food_allowance;
                                            row.car_allowance = data.car_allowance;
                                            row.mobile_allowance = data.mobile_allowance;
                                            row.overtime_hourly_rate = data.overtime_hourly_rate;
                                            row.fuel_allowance = data.fuel_allowance;
                                            row.leave_encashment_amount_per_day = data.leave_encashment_amount_per_day;
                                            row.job_well_done = data.job_well_done;
                                            row.position_level = data.position_level;
                                            row.attendance_bonus = data.attendance_bonus;
                                            row.holiday_overtime_rate = data.holiday_overtime_rate;
                                            row.increment_amount = data.increment_amount;
                                            row.increment_date = data.date;
                                            
                                            frm.save();
                                            frm.refresh_field('components');
                                        }
                                    }
                                });
                                d.hide();
                            },
                            function() {
                                frappe.show_alert({
                                    message: __('Operation cancelled'),
                                    indicator: 'orange'
                                });
                            }
                        );
                    }
                });

                d.show();
            });
        }
    }
});