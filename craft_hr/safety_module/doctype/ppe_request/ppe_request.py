import frappe
from frappe.model.document import Document
from frappe.utils import add_days, flt, getdate

class PPERequest(Document):
    def on_submit(self):
        ppe_authorization = frappe.new_doc("PPE Authorization")

        ppe_authorization.ppe_request = self.name
        ppe_authorization.employee = self.employee
        ppe_authorization.date_of_joining = self.date_of_joining
        ppe_authorization.employee_name = self.employee_name
        ppe_authorization.designation = self.designation
        ppe_authorization.ppe_request_date = self.ppe_request_date
        ppe_authorization.store_location = self.store_location
        ppe_authorization.source_warehouse = self.source_warehouse
        ppe_authorization.category = self.category

        for item in self.items:
            ppe_authorization.append(
                "items",
                {
                    "item_code": item.item_code,
                    "quantity": item.quantity,
                    "requested_quantity": item.quantity,
                    "uom": item.uom,
                    "item_name": item.item_name,
                    "description": item.description,
                    "issued_item_damaged": item.issued_item_damaged,
                },
            )

        self.update_ppe_authorization(ppe_authorization)

        ppe_authorization.insert()

        frappe.msgprint(
            f"PPE Authorization {ppe_authorization.name} has been created.", alert=True
        )

    def update_ppe_authorization(self, ppe_authorization):
        for item in ppe_authorization.items:
            custom_duration = frappe.db.get_value("Item", item.item_code, "custom_duration")

            if custom_duration is not None:
                duration = int(custom_duration)
                request_date = getdate(self.ppe_request_date)

                total_issue_qty_query = f"""
                    SELECT COUNT(*) as total_issue_qty
                    FROM
                        `tabPPE Authorization` pa
                    JOIN
                        `tabPPE Auth Items` pai ON pa.name = pai.parent
                    JOIN
                        `tabPPE Request` pr ON pa.ppe_request = pr.name
                    JOIN
                        `tabPPE Items` i ON pr.name = i.parent
                    WHERE
                        pa.docstatus = 1  -- Ensure PPE Authorization is submitted
                        AND pai.status = 'Approved'  -- Only include approved items
                        AND pr.employee = {frappe.db.escape(self.employee)}
                        AND pr.docstatus = 1  -- Ensure PPE Request is submitted
                        AND DATE_ADD(DATE(pr.ppe_request_date), INTERVAL {duration} DAY) >= DATE({frappe.db.escape(request_date)})
                        AND i.item_code = {frappe.db.escape(item.item_code)}
                        AND pr.name != {frappe.db.escape(ppe_authorization.ppe_request)}
                """

                total_issue_qty_result = frappe.db.sql(total_issue_qty_query, as_dict=True)
                total_issue_qty = total_issue_qty_result[0].get('total_issue_qty', 0) if total_issue_qty_result else 0

                last_issued_on_query = f"""
                    SELECT
                        MAX(pr.ppe_request_date) as last_issued_on
                    FROM
                        `tabPPE Authorization` pa
                    JOIN
                        `tabPPE Auth Items` pai ON pa.name = pai.parent
                    JOIN
                        `tabPPE Request` pr ON pa.ppe_request = pr.name
                    JOIN
                        `tabPPE Items` i ON pr.name = i.parent
                    WHERE
                        pa.docstatus = 1  -- Ensure PPE Authorization is submitted
                        AND pai.status = 'Approved'  -- Only include approved items
                        AND pr.employee = {frappe.db.escape(self.employee)}
                        AND pr.docstatus = 1  -- Ensure PPE Request is submitted
                        AND DATE_ADD(DATE(pr.ppe_request_date), INTERVAL {duration} DAY) >= DATE({frappe.db.escape(self.ppe_request_date)})
                        AND i.item_code = {frappe.db.escape(item.item_code)}
                        AND pr.name != {frappe.db.escape(ppe_authorization.ppe_request)}
                """

                last_issued_on_result = frappe.db.sql(last_issued_on_query, as_dict=True)
                last_issued_on = last_issued_on_result[0].get('last_issued_on') if last_issued_on_result else None

                item.total_issue_qty = total_issue_qty
                item.last_issued_on = last_issued_on



    def validate(self, method=None):
        for item in self.items:
            custom_replace = frappe.db.get_value("Item", item.item_code, "custom_replace")
            
            if item.issued_item_damaged:
                if not custom_replace:
                    frappe.throw(
                        f"Row #{item.idx}: Replacement is not allowed for the item '{item.item_code}'."
                    )
                continue

            warehouse_company = frappe.db.get_value(
                "Warehouse", {"name": self.source_warehouse}, "company"
            )

            if warehouse_company != self.company:
                frappe.throw(
                    f"Warehouse '{self.source_warehouse}' does not belong to the company '{self.company}'."
                )

            item_in_warehouse = frappe.db.exists(
                "Bin", {"item_code": item.item_code, "warehouse": self.source_warehouse}
            )

            if not item_in_warehouse:
                frappe.throw(
                    f"Row #{item.idx}: Item '{item.item_code}' does not exist in the warehouse '{self.source_warehouse}'."
                )

            max_issue_quantity, custom_duration = frappe.db.get_value(
                "Item", item.item_code, ["max_issue_quantity", "custom_duration"]
            )

            if max_issue_quantity and custom_duration:
                from_date = add_days(getdate(self.ppe_request_date), -flt(custom_duration))

                employee_issued_count_query = f"""
                    SELECT SUM(pai.quantity) as issued_quantity
                    FROM `tabPPE Authorization` pa
                    JOIN `tabPPE Auth Items` pai ON pa.name = pai.parent
                    JOIN `tabPPE Request` pr ON pr.name = pa.ppe_request
                    WHERE pr.docstatus = 1
                    AND pa.docstatus = 1
                    AND pr.employee = {frappe.db.escape(self.employee)}
                    AND pai.item_code = {frappe.db.escape(item.item_code)}
                    AND pai.status = 'Approved'
                    AND pr.ppe_request_date BETWEEN {frappe.db.escape(str(from_date))} AND {frappe.db.escape(str(self.ppe_request_date))}                """

                employee_issued_count_result = frappe.db.sql(employee_issued_count_query, as_dict=True)
                issued_quantity = employee_issued_count_result[0].get("issued_quantity", 0) or 0

                total_requested_quantity = issued_quantity + item.quantity

                if total_requested_quantity > max_issue_quantity:
                    if issued_quantity == 0:
                        frappe.throw(
                            f"Row #{item.idx}: The item '{item.item_code}' exceeds the maximum issue quantity of {max_issue_quantity}."
                        )
                    else:
                        frappe.throw(
                            f"Row #{item.idx}: The item '{item.item_code}' exceeds the maximum issue quantity of {max_issue_quantity}. You can request the item again only if it is damaged and eligible for replacement."
                        )

                if issued_quantity >= max_issue_quantity:
                    frappe.throw(
                        f"Row #{item.idx}: The item '{item.item_code}' exceeds the maximum issue quantity of {max_issue_quantity}."
                    )







