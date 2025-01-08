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
                        row.car_allowance = components.car_allowance;
                        row.mobile_allowance = components.mobile_allowance;
                        row.overtime_hourly_rate = components.overtime_hourly_rate;
                        row.fuel_allowance = components.fuel_allowance;
                        row.leave_encashment_amount_per_day = components.leave_encashment_amount_per_day;
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
            from_date: lastComponent.increment_date,
            docstatus: 1
        }, 'name', function(result) {
            const confirmMessage = result.name
                ? __('Are you sure you want to delete the last row? This will also require you to delete the corresponding Salary Structure Assignment: {0}.', [result.name])
                : __('Are you sure you want to delete the last row?');
    
            frappe.confirm(confirmMessage, function() {
                frm.doc.components.pop();
                frm.dirty();             
                frm.save().then(() => {  
                    frm.refresh_field('components');
                    frappe.show_alert({
                        message: __('Row deleted successfully'),
                        indicator: 'green'
                    });
                }).catch(err => {
                    console.error("Error saving the form:", err);
                });
            });
        });
    }
    ,
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Add Salary'), function() {
                const default_components = frm.doc.components[frm.doc.components.length - 1] || {};
    
                let default_values = {
                    basic: default_components.basic || 0,
                    hra: default_components.hra || 0,
                    transport_allowance: default_components.transport_allowance || 0,
                    cost_of_living_allowance: default_components.cost_of_living_allowance || 0,
                    other_allowance: default_components.other_allowance || 0,
                    car_allowance: default_components.car_allowance || 0,
                    mobile_allowance: default_components.mobile_allowance || 0,
                    overtime_hourly_rate: default_components.overtime_hourly_rate || 0,
                    fuel_allowance: default_components.fuel_allowance || 0,
                    leave_encashment_amount_per_day: default_components.leave_encashment_amount_per_day || 0,
                    holiday_overtime_rate: default_components.holiday_overtime_rate || 0
                };
    
                let d = new frappe.ui.Dialog({
                    title: 'Add Salary Details',
                    fields: [
                        { fieldname: 'salary_increment', label: 'Salary Increment', fieldtype: 'Link', options: 'Salary Increment', default: frm.doc.name },
                        { fieldname: 'employee', label: 'Employee', fieldtype: 'Link', options: 'Employee', default: frm.doc.employee, read_only: 1 },
                        { fieldname: 'column1', label: '', fieldtype: 'Column Break' },
                        { fieldname: 'date', label: 'Date', fieldtype: 'Date', default: frappe.datetime.get_today() },
                        { fieldname: 'salary_structure', label: 'Salary Structure', fieldtype: 'Link', options: 'Salary Structure', reqd: 1 },
                        { fieldname: 'section1', label: '', fieldtype: 'Section Break' },
                        { fieldname: 'basic', label: 'Basic', fieldtype: 'Currency', default: default_values.basic },
                        { fieldname: 'hra', label: 'HRA', fieldtype: 'Currency', default: default_values.hra },
                        { fieldname: 'transport_allowance', label: 'Transport Allowance', fieldtype: 'Currency', default: default_values.transport_allowance },
                        { fieldname: 'cost_of_living_allowance', label: 'Cost of Living Allowance', fieldtype: 'Currency', default: default_values.cost_of_living_allowance },
                        { fieldname: 'column2', label: '', fieldtype: 'Column Break' },
                        { fieldname: 'other_allowance', label: 'Other Allowance', fieldtype: 'Currency', default: default_values.other_allowance },
                        { fieldname: 'car_allowance', label: 'Car Allowance', fieldtype: 'Currency', default: default_values.car_allowance },
                        { fieldname: 'mobile_allowance', label: 'Mobile Allowance', fieldtype: 'Currency', default: default_values.mobile_allowance },
                        { fieldname: 'overtime_hourly_rate', label: 'Overtime Hourly Rate', fieldtype: 'Currency', default: default_values.overtime_hourly_rate },
                        { fieldname: 'column3', label: '', fieldtype: 'Column Break' },
                        { fieldname: 'fuel_allowance', label: 'Fuel Allowance', fieldtype: 'Currency', default: default_values.fuel_allowance },
                        { fieldname: 'leave_encashment_amount_per_day', label: 'Leave Encashment Amount Per Day', fieldtype: 'Currency', default: default_values.leave_encashment_amount_per_day },
                        { fieldname: 'holiday_overtime_rate', label: 'Holiday Overtime Rate', fieldtype: 'Currency', default: default_values.holiday_overtime_rate },
                        { fieldname: 'section2', label: '', fieldtype: 'Section Break' },
                        { fieldname: 'increment_amount', label: 'Increment Amount', fieldtype: 'Currency', read_only: 1 },
                    ],
                    size: 'extra-large',
                    primary_action_label: 'Save',
                    primary_action: function(data) {
                        if (data.increment_amount > 0) {
                            frappe.confirm(
                                'Are you sure you want to submit?',
                                function() {
                                    frappe.call({
                                        method: 'frappe.client.submit',
                                        args: {
                                            doc: {
                                                doctype: 'Salary Structure Assignment',
                                                employee: data.employee,
                                                custom_salary_increment: data.salary_increment,
                                                salary_structure: data.salary_structure,
                                                from_date: data.date,
                                                sc_basic: data.basic,
                                                sc_hra: data.hra,
                                                sc_transport: data.transport_allowance,
                                                sc_cola: data.cost_of_living_allowance,
                                                sc_other: data.other_allowance,
                                                sc_car: data.car_allowance,
                                                sc_mobile: data.mobile_allowance,
                                                ot_rate: data.overtime_hourly_rate,
                                                sc_fuel: data.fuel_allowance,
                                                custom_leave_encashment_amount_per_day: data.leave_encashment_amount_per_day,
                                                holiday_ot_rate: data.holiday_overtime_rate
                                            }
                                        },
                                        callback: function(response) {
                                            if (response.message) {
                                                let assignment_name = response.message.name;
    
                                                frappe.show_alert({
                                                    message: __('Salary Structure Assignment created successfully'),
                                                    indicator: 'green'
                                                });
    
                                                let row = frm.add_child('components');
                                                Object.assign(row, {
                                                    basic: data.basic,
                                                    hra: data.hra,
                                                    transport_allowance: data.transport_allowance,
                                                    cost_of_living_allowance: data.cost_of_living_allowance,
                                                    other_allowance: data.other_allowance,
                                                    car_allowance: data.car_allowance,
                                                    mobile_allowance: data.mobile_allowance,
                                                    overtime_hourly_rate: data.overtime_hourly_rate,
                                                    fuel_allowance: data.fuel_allowance,
                                                    leave_encashment_amount_per_day: data.leave_encashment_amount_per_day,
                                                    holiday_overtime_rate: data.holiday_overtime_rate,
                                                    increment_amount: data.increment_amount,
                                                    increment_date: data.date
                                                });
    
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
                        } else {
                            frappe.msgprint(__('Increment Amount must be greater that zero to create a new Salary Structure Assignment'));
                        }
                    }
                });
    
                Object.keys(default_values).forEach(field => {
                    d.fields_dict[field].df.onchange = () => {
                        let increment_total = 0;
    
                        Object.keys(default_values).forEach(key => {
                            let current_value = d.get_value(key) || 0;
                            let default_value = default_values[key];
                            increment_total += current_value - default_value;
                        });
    
                        d.set_value('increment_amount', increment_total);
                    };
                });
    
                d.show();
            });
        }
    }
    });