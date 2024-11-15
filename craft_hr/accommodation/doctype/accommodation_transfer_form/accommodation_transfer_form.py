# Copyright (c) 2024, Craft Interactive and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AccommodationTransferForm(Document):
    def validate(self):
        if self.accommodation_type == "Allocation":
            if self.to_bed_no:
                bed = frappe.get_doc("Bed",{"name" : self.to_bed_no})
                bed.floor_no = self.to_floor_no
                bed.room_no = self.to_room_no
                bed.building_name = self.to_building_name
                bed.employee = self.employee
                bed.status = "Allocated"
                bed.save()

        elif self.accommodation_type == "Transfer":
            if self.to_bed_no:
                bed = frappe.get_doc("Bed",{"name" : self.to_bed_no})
                bed.floor_no = self.to_floor_no
                bed.room_no = self.to_room_no
                bed.building_name = self.to_building_name
                bed.employee = self.employee
                bed.status = "Allocated"
                bed.save()
        
        elif self.accommodation_type == "Exit":
            if self.employee:
                employee = frappe.get_doc("Employee",{"name":self.employee})
                employee.custom_building_name = ''
                employee.custom_floor_number = ''
                employee.custom_room_number = ''
                employee.custom_bed_number = ''
                employee.save()

            if self.from_bed_no:
                bed = frappe.get_doc("Bed",{"name" : self.from_bed_no})
                bed.floor_no = ''
                bed.room_no = ''
                bed.building_name = ''
                bed.employee = ''
                bed.status = "Vacant"
                bed.save()

# @frappe.whitelist()
# def get_bed_details(employee):
# 	bed = frappe.db.get_value('Bed', {'employee': employee}, ['name', 'room_no'], as_dict=True)
# 	print(bed, 5555555555)
# 	# if bed:
# 	# 	return bed
# 	# else:
# 	# 	return None

# 	if bed:
# 		room = frappe.db.get_value('Room', bed.room_no, ['floor_no'], as_dict=True)
		
# 		if room:
# 			floor = frappe.db.get_value('Floor', room.floor_no, ['building_name'], as_dict=True)
			
# 			if floor:
# 				bed_details = {
# 					'bed_no': bed.name,
# 					'room_no': bed.room_no,
# 					'floor_no': room.floor_no,
# 					'building_name': floor.building_name
# 				}
# 				return bed_details
# 	return None

# # @frappe.whitelist()
# # def exit_employee(employee):
# #     bed = frappe.db.get_value('Bed', {'employee': employee}, ['name'], as_dict=True)
    
# #     if bed:
# #         frappe.db.set_value('Bed', bed.name, {
# #             'employee': None,
# #             'status': 'Vacant'
# #         })
# #         frappe.db.commit()
# #         return 'success'
    
# #     return 'failure'


# # @frappe.whitelist()
# # def transfer_employee_bed(employee, new_bed):
# #     current_bed = frappe.db.get_value('Bed', {'employee': employee}, ['name'], as_dict=True)
    
# #     if current_bed:
# #         # Clear the current bed
# #         frappe.db.set_value('Bed', current_bed.name, {
# #             'employee': None,
# #             'status': 'Vacant'
# #         })
        
# #     # Assign the employee to the new bed
# #     frappe.db.set_value('Bed', new_bed, {
# #         'employee': employee,
# #         'status': 'Occupied'
# #     })
    
# #     frappe.db.commit()
# #     return 'success'


# # @frappe.whitelist()
# # def exit_employee(employee, docname):
# #     bed = frappe.db.get_value('Bed', {'employee': employee}, ['name', 'bed_no'], as_dict=True)
    
# #     if bed:
# #         frappe.db.set_value('Bed', bed.name, {
# #             'employee': None,
# #             'status': 'Vacant'
# #         })
        
# #         # Update the Accommodation Transfer Form document
# #         doc = frappe.get_doc('Accommodation Transfer Form', docname)
# #         doc.append('allocations', {
# #             'from_bed_no': bed.name,
# #             'to_bed_no': None
# #         })
# #         doc.save()
        
# #         frappe.db.commit()
# #         return 'success'
    
# #     return 'failure'

# # @frappe.whitelist()
# # def transfer_employee_bed(employee, new_bed, docname):
# #     current_bed = frappe.db.get_value('Bed', {'employee': employee}, ['name', 'bed_no'], as_dict=True)
    
# #     if current_bed:
# #         # Clear the current bed
# #         frappe.db.set_value('Bed', current_bed.name, {
# #             'employee': None,
# #             'status': 'Vacant'
# #         })
        
# #     # Assign the employee to the new bed
# #     frappe.db.set_value('Bed', new_bed, {
# #         'employee': employee,
# #         'status': 'Occupied'
# #     })
    
# #     # Update the Accommodation Transfer Form document
# #     doc = frappe.get_doc('Accommodation Transfer Form', docname)
# #     doc.append('allocations', {
# #         'from_bed_no': current_bed.name if current_bed else None,
# #         'to_bed_no': new_bed
# #     })
# #     doc.save()
    
# #     frappe.db.commit()
# #     return 'success'


# @frappe.whitelist()
# def exit_employee(employee, docname):
#     bed = frappe.db.get_value('Bed', {'employee': employee}, ['name', 'bed_no'], as_dict=True)
    
#     if bed:
#         frappe.db.set_value('Bed', bed.name, {
#             'employee': None,
#             'status': 'Vacant'
#         })
        
#         # Update the Accommodation Transfer Form document
#         doc = frappe.get_doc('Accommodation Transfer Form', docname)
#         doc.append('allocations', {
#             'from_bed_no': bed.name,
#             'to_bed_no': None
#         })
#         doc.save(ignore_permissions=True)
        
#         frappe.db.commit()
#         return 'success'
    
#     return 'failure'

# @frappe.whitelist()
# def transfer_employee_bed(employee, new_bed, docname):
#     current_bed = frappe.db.get_value('Bed', {'employee': employee}, ['name', 'bed_no'], as_dict=True)
    
#     if current_bed:
#         # Clear the current bed
#         frappe.db.set_value('Bed', current_bed.name, {
#             'employee': None,
#             'status': 'Vacant'
#         })
        
#     # Assign the employee to the new bed
#     frappe.db.set_value('Bed', new_bed, {
#         'employee': employee,
#         'status': 'Occupied'
#     })
    
#     # Update the Accommodation Transfer Form document
#     doc = frappe.get_doc('Accommodation Transfer Form', docname)
#     doc.append('allocations', {
#         'from_bed_no': current_bed['name'] if current_bed else None,
#         'to_bed_no': new_bed
#     })
#     doc.save(ignore_permissions=True)
    
#     frappe.db.commit()
#     return 'success'
