from datetime import datetime, date, timedelta

def stints_to_table(stints, starting_tires):
    rows = []

    prev_stint = {}
    tires_left = int(starting_tires)
    for stint in stints:
        
        stint_time = "00:00:00"
        if bool(prev_stint):
            t1 = datetime.strptime(prev_stint.get('pit_end_time'), "%H:%M:%S").time()
            t2 = datetime.strptime(stint.get('pit_end_time'), "%H:%M:%S").time()

            dt1 = datetime.combine(date.today(), t1)
            dt2 = datetime.combine(date.today(), t2)
            stint_time = dt1 - dt2

        tires_changed = int(stint.get("tires_changed"))
        tires_left = tires_left - tires_changed
    

        rows.append([
            stint.get("driver"),
            "✅",
            stint.get("pit_end_time"),
            tires_changed,
            tires_left,
            stint_time
        ])
        prev_stint = stint

    avg_stint_time = '0:42:30'

    while not is_last_stint(prev_stint.get('pit_end_time'), avg_stint_time):
        t1 = datetime.strptime(prev_stint.get('pit_end_time'), "%H:%M:%S").time()
        t2 = datetime.strptime(avg_stint_time, "%H:%M:%S").time()

        # Convert t1 to a datetime
        dt = datetime.combine(datetime.today(), t1)

        # Convert t2 to a timedelta
        delta = timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)

        # Subtract the timedelta
        dt_minus = dt - delta

        # Get the time part again
        t1_minus = dt_minus.time()
        prev_stint['pit_end_time'] = str(t1_minus)
        tires_changed = int(stint.get("tires_changed"))
        tires_left = tires_left - tires_changed
    

        rows.append([
            stint.get("driver"),
            "❌",
            stint.get("pit_end_time"),
            tires_changed,
            tires_left,
            stint_time
        ])
        prev_stint = stint

    return rows

def is_last_stint(pit_end_time, avg_stint_time):
    t1 = datetime.strptime(pit_end_time, "%H:%M:%S").time()
    t2 = datetime.strptime(avg_stint_time, "%H:%M:%S").time()
    dt1 = datetime.combine(date.today(), t1)
    dt2 = datetime.combine(date.today(), t2)
    stint_time = dt1 - dt2

    if str(stint_time).startswith("-1 day"):
        return True

    return False