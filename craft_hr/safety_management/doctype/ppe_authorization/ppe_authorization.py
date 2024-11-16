import frappe
from frappe.model.document import Document
from erpnext.manufacturing.doctype.bom.bom import get_valuation_rate

class PPEAuthorization(Document):
    def validate(self):
        self.validate_ppe_authorization()

    def on_submit(self):
        if any(item.expense_type == "Expense Company" for item in self.items):
            self.create_and_submit_stock_entry()
        self.update_ppe_request_remarks()

    def create_and_submit_stock_entry(self):
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "PPE Issue"
        stock_entry.company = self.company
        stock_entry.from_warehouse = self.source_warehouse
        stock_entry.custom_ppe_authorization = self.name

        added_items = False

        for item in self.items:
            if item.status == "Approved" and item.expense_type == "Expense Company":
                stock_entry.append(
                    "items",
                    {
                        "item_code": item.item_code,
                        "qty": item.quantity,
                        "uom": item.uom,
                        "s_warehouse": self.source_warehouse,
                        "description": item.description,
                    },
                )
                added_items = True

        if added_items:
            stock_entry.insert(ignore_permissions=True)
            stock_entry.submit()
            frappe.msgprint(
                f"Stock Entry {stock_entry.name} created and submitted successfully.",
                alert=True,
            )
        else:
            frappe.msgprint("No approved items to create a stock entry.", alert=True)

    def validate_ppe_authorization(self):
        for item in self.items:
            valuation = valuation_rate(item_code=item.item_code)
            if valuation:
                item.amount = valuation

            bin_qty = frappe.db.get_value(
                "Bin",
                {"item_code": item.item_code, "warehouse": self.source_warehouse},
                "actual_qty",
            )
            item.stock_available = bin_qty if bin_qty else 0

    def update_ppe_request_remarks(self):
        ppe_request = frappe.get_doc("PPE Request", self.ppe_request)

        for auth_item in self.items:
            for req_item in ppe_request.items:
                if auth_item.item_code == req_item.item_code:
                    req_item.remarks = auth_item.remarks

        ppe_request.save()
        frappe.msgprint(f"PPE Request {ppe_request.name} updated with remarks.", alert=True)


@frappe.whitelist()
def valuation_rate(item_code=None):
    company = frappe.db.get_list("Company", pluck="name")[0]
    return get_valuation_rate(data={"item_code": item_code, "company": company})
