# Copyright (c) 2024, craft@gmail.com and contributors
# For license information, please see license.txt

import frappe
import json

from frappe.model.document import Document

class Expenses(Document):
	pass


@frappe.whitelist()
def create_fuel_vehicle_logs(fuel_expense):
    fuel_expense = json.loads(fuel_expense)
    for row in fuel_expense:
        vehicle_log = frappe.get_doc({
            'doctype': 'Vehicle Log',
            'license_plate': row['vehicle'],
            'fuel_qty': row['quantity'],
            'price': row['total_amount'],
            'odometer': row['current_odometer_value'],
            'company': row['company'],
            'date' : row['date']
        })
        vehicle_log.insert()
        vehicle_log.submit()
    return True

@frappe.whitelist()
def create_service_vehicle_logs(service_expense):
    import json
    service_expense = json.loads(service_expense)
    vehicle_log_map = {}
    for row in service_expense:
        if row['vehicle'] not in vehicle_log_map:
            vehicle_log_map[row['vehicle']] = frappe.get_doc({
                'doctype': 'Vehicle Log',
                'license_plate': row['vehicle'],
                'date': row['date'],
                'odometer': row['current_odometer_value'],
                'service_detail': []
            })
        vehicle_log_map[row['vehicle']].append('service_detail', {
            'service_item': row['service_item'],
            'category': row['category'],
            'type': row['type'],
            'frequency': row['frequency'],
            'expense_amount': row['expense']
        })
    for vehicle_log in vehicle_log_map.values():
        vehicle_log.insert()
        vehicle_log.submit()
    return True
