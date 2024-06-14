import frappe
import datetime
from frappe.utils import (time_diff_in_hours)
from datetime import timedelta

def before_validate(doc, method):
    start = datetime.datetime.strptime(doc.start_time, "%H:%M:%S")
    end = datetime.datetime.strptime(doc.end_time, "%H:%M:%S")
    if doc.is_night_shift:
        end += timedelta(hours=24)
    shift_hours = time_diff_in_hours(end,start)
    doc.db_set('shift_hours',shift_hours)
