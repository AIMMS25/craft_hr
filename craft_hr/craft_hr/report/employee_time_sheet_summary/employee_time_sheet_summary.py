# Copyright (c) 2024, Craftinteractive and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _

def execute(filters=None):
    if filters.get("summarized_view"):
        result = get_data(filters)
        summarized_columns = get_summarized_columns()
        summarized_data = generate_summarized_data(result[0])
        return summarized_columns, summarized_data
    else:
        result = get_data(filters)
        columns = get_columns(result[1])
        return columns, result[0]

def get_data(filters):
    attendance_data = frappe.db.sql("""
        SELECT 
            at.employee AS employee,
            at.employee_name AS employee_name,
            at.attendance_date AS attendance_date,
            ec.time AS time,
            at.ot AS overtime_hours,
            at.hot AS holiday_overtime_hours,
            at.working_hours,
            at.shift_hours,
            at.late_hours AS late_hours,
            ec.shift AS shift,
            at.status AS status,
            ec.log_type
        FROM
            `tabEmployee Checkin` AS ec
        LEFT JOIN
            `tabAttendance` AS at ON ec.employee = at.employee
        WHERE
            at.attendance_date BETWEEN DATE(ec.shift_start) AND DATE(ec.shift_end)
            AND DATE(at.attendance_date) BETWEEN DATE(%(from_date)s) AND DATE(%(to_date)s)
            {employee_filter}
        ORDER BY ec.time ASC
    """.format(
        employee_filter="AND at.employee=%(employee)s" if filters.get("employee") else ""
    ), 
    {
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "employee": filters.get("employee")
    }, as_dict=True)


    for entry in attendance_data:
        entry["employee_name"] = entry.get("employee_name") or frappe.db.get_value("Employee", entry["employee"], "employee_name")

    
    emp_wise_data = {}
    for entry in attendance_data:
        emp_wise_data.setdefault(entry["employee"], []).append(entry)

    data, max_count = [], 0
    for employee, entries in emp_wise_data.items():
        date_wise_data = {}
        for entry in entries:
            date_wise_data.setdefault(entry["attendance_date"], []).append(entry)

        for date, logs in date_wise_data.items():
            row = build_attendance_row(logs, date)
            row["employee_name"] = logs[0].get("employee_name")
            counter = add_checkin_data(row, logs)
            max_count = max(max_count, counter)
            data.append(row)

        # Add holiday data
        holiday_rows = get_holiday_rows(employee, filters)
        for holiday_row in holiday_rows:
            holiday_row["employee_name"] = frappe.db.get_value("Employee", employee, "employee_name")
        data.extend(holiday_rows)


    data = sorted(data, key=lambda x: x['attendance_date'])
    return [data, max_count]


def build_attendance_row(logs, date):
    """ Helper function to calculate attendance details and build a row """
    first_log = logs[0]
    absent_hours = max(first_log.shift_hours - first_log.working_hours - 0.5, 0)
    ot_hours = max(first_log.working_hours - first_log.shift_hours, 0)

    row = {
        "employee": first_log.employee,
        "employee_name": first_log.employee_name,
        "attendance_date": date,
        "day": frappe.utils.get_weekday(date),
        "overtime_hours": first_log.overtime_hours,
        "holiday_overtime_hours": first_log.holiday_overtime_hours,
        "working_hours": first_log.working_hours,
        "shift_hours": first_log.shift_hours,
        "absent_hours": absent_hours,
        "ot_hours": ot_hours,
        "late_hours": first_log.late_hours,
        "shift": first_log.shift,
        "status": get_status_html(first_log.status)
    }
    return row

def add_checkin_data(row, logs):
    """ Append check-in times and log types to the row """
    for idx, log in enumerate(logs):
        row[f"checkin{idx + 1}"] = f"{str(log.time).split(' ')[1][:5]}-{log.log_type}"
    return len(logs)

def get_status_html(status):
    """ Generate HTML for status color-coding """
    color = {
        "Present": "green",
        "Absent": "orange",
        "On Leave": "blue",
        "Half Day": "grey"
    }.get(status, "black")
    return f"<span style='color: {color}'>{status}</span>"

def get_holiday_rows(employee, filters):
    """ Retrieve holidays within the date range for the employee """
    holiday_list_name = frappe.db.get_value("Employee", employee, "holiday_list")
    if not holiday_list_name:
        return []

    holidays = frappe.get_all(
        "Holiday",
        filters={
            "parent": holiday_list_name,
            "holiday_date": ["between", [filters.get("from_date"), filters.get("to_date")]]
        },
        fields=["holiday_date"]
    )

    return [
        {
            "employee": employee,
            "attendance_date": holiday.holiday_date,
            "day": frappe.utils.get_weekday(holiday.holiday_date),
            "status": "<span style='color: red'>Holiday</span>"
        }
        for holiday in holidays
    ]

def get_columns(max_count):
    """ Define columns based on max_count for check-in fields """
    name_columns = [
        {"fieldname": "attendance_date", "label": _("Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "day", "label": _("Day"), "fieldtype": "Data", "width": 100},
        {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Data", "width": 200, "hidden": 1},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Select", "width": 100}
    ]

    for i in range(max_count):
        name_columns.append({
            "fieldname": f"checkin{i + 1}", "label": _("Time"), "fieldtype": "Data", "width": 100
        })

    additional_columns = [
        {"fieldname": "shift_hours", "label": _("Shift Hours"), "fieldtype": "Float", "width": 100},
        {"fieldname": "working_hours", "label": _("Working Hours"), "fieldtype": "Float", "width": 100},
        {"fieldname": "absent_hours", "label": _("Absent Hours"), "fieldtype": "Float", "width": 100},
        {"fieldname": "ot_hours", "label": _("OT Hours"), "fieldtype": "Float", "width": 100},
        {"fieldname": "late_hours", "label": _("Late Hours"), "fieldtype": "Float", "width": 100},
        {"fieldname": "shift", "label": _("Shift"), "fieldtype": "Data", "width": 200}
    ]

    return name_columns + additional_columns

def get_summarized_columns():
    return [
        {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Data", "width": 180},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 370},
        {"fieldname": "total_shift_hours", "label": _("Total Shift Hours"), "fieldtype": "Float", "width": 130},
        {"fieldname": "total_working_hours", "label": _("Total Working Hours"), "fieldtype": "Float", "width": 130},
        {"fieldname": "total_absent_hours", "label": _("Total Absent Hours"), "fieldtype": "Float", "width": 130},
        {"fieldname": "total_ot_hours", "label": _("Total OT Hours"), "fieldtype": "Float", "width": 130},
        {"fieldname": "total_late_hours", "label": _("Total Late Hours"), "fieldtype": "Float", "width": 130}
    ]

def generate_summarized_data(emp_data):
    summarized_data = []
    processed_employees = set()


    for entry in emp_data:
        employee_id = entry['employee']
        if employee_id in processed_employees:
            continue


        totals = {
            "total_shift_hours": 0,
            "total_working_hours": 0,
            "total_late_hours": 0,
            "total_absent_hours": 0,
            "total_ot_hours": 0
        }


        for rec in emp_data:
            if rec['employee'] == employee_id:
                totals["total_shift_hours"] += rec.get("shift_hours", 0)
                totals["total_working_hours"] += rec.get("working_hours", 0)
                totals["total_late_hours"] += rec.get("late_hours", 0)
                totals["total_absent_hours"] += rec.get("absent_hours", 0)
                totals["total_ot_hours"] += rec.get("ot_hours", 0)


        summarized_row = {
            "employee": employee_id,
            "employee_name": entry.get("employee_name", ""),
            "total_shift_hours": totals["total_shift_hours"],
            "total_working_hours": totals["total_working_hours"],
            "total_absent_hours": totals["total_absent_hours"],
            "total_ot_hours": totals["total_ot_hours"],
            "total_late_hours": totals["total_late_hours"]
        }
        summarized_data.append(summarized_row)
        processed_employees.add(employee_id)

    return summarized_data
