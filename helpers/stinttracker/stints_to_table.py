from datetime import datetime, date, timedelta, time

def stints_to_table(stints, starting_tires, starting_time):
    rows = []

    prev_stint = {}
    tires_left = int(starting_tires)
    stint_times = []
    start_of_stint = 0
    for i, stint in enumerate(stints):
        
        stint_time = "00:00:00"
        t1 = ""
        if bool(prev_stint):
            t1 = datetime.strptime(prev_stint.get('pit_end_time'), "%H:%M:%S").time()
        else:
            t1 = datetime.strptime(normalize_24h_time(starting_time), "%H:%M:%S").time()
            
        t2 = datetime.strptime(stint.get('pit_end_time'), "%H:%M:%S").time()

        dt1 = datetime.combine(date.today(), t1)
        dt2 = datetime.combine(date.today(), t2)

        # If start time is earlier, it must be the next day
        if dt1 < dt2:
            dt1 += timedelta(days=1)

        stint_time = dt1 - dt2
        stint_times.append(stint_time)

        tires_changed = int(stint.get("tires_changed"))
        tires_left = tires_left - tires_changed

        stint_amounts = i - start_of_stint
        stint_type = get_stint_type(stint_amounts + 1)
        
        if tires_changed:
            stint_type = ""
            if start_of_stint == i:
                stint_type = "Single"
            start_of_stint = i + 1
        
        # If it's more than a double stint
        if stint_amounts and not tires_changed:
            rows[start_of_stint][0] = get_stint_type(stint_amounts + 1)
            stint_type = ""

        rows.append([
            stint_type,
            stint.get("driver"),
            "✅",
            stint.get("pit_end_time"),
            tires_changed,
            tires_left,
            stint_time
        ])
        prev_stint = stint

    mean_stint_time = calc_mean_stint_time(stint_times)

    if prev_stint:
        while not is_last_stint(prev_stint.get('pit_end_time'), timedelta_to_time(mean_stint_time)):
            t1 = datetime.strptime(prev_stint.get('pit_end_time'), "%H:%M:%S").time()
            t2 = timedelta_to_time(mean_stint_time)

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
                "Single",
                stint.get("driver"),
                "❌",
                stint.get("pit_end_time"),
                tires_changed,
                tires_left,
                mean_stint_time
            ])
            prev_stint = stint
    else:
        print("No stint exists")

    return rows

def calc_mean_stint_time(stint_times):
    if not stint_times:
        return time(0, 0, 0)

    total = sum(stint_times, timedelta(0))
    mean = total / len(stint_times)

    total_seconds = int(mean.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # time() requires hours < 24 → clamp or wrap
    hours %= 24

    t = time(hours, minutes, seconds)

    return timedelta(
        hours=t.hour,
        minutes=t.minute,
        seconds=t.second,
        microseconds=t.microsecond
    )

def is_last_stint(pit_end_time, mean_stint_time):
    t1 = datetime.strptime(pit_end_time, "%H:%M:%S").time()
    t2 = mean_stint_time
    dt1 = datetime.combine(date.today(), t1)
    dt2 = datetime.combine(date.today(), t2)
    stint_time = dt1 - dt2

    if str(stint_time).startswith("-1 day"):
        return True

    return False

def normalize_24h_time(time_str: str) -> str:
    if time_str.startswith("24:"):
        return "00:" + time_str[3:]
    return time_str

def timedelta_to_time(td):
    """
    Convert a timedelta to a datetime.time object.
    Hours are modulo 24.
    """
    total_seconds = int(td.total_seconds())  # ignore microseconds for now
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours %= 24  # wrap around if > 24
    return time(hour=hours, minute=minutes, second=seconds)

def get_stint_type(stint_amounts):
    match stint_amounts:
        case 0:
            return "Single"
        case 1:
            return "Double"
        case 2:
            return "Triple"
        case 3:
            return "Quadruple"
        case 4:
            return "Quadruple"
        case 5:
            return "Quintuple"
        case 6:
            return "Sextuple"
        case 7:
            return "Septuple"
        case 8:
            return "Octuple"
        case 9:
            return "Nonuple"
        case 10:
            return "Decuple"
        case _:
            return "Unknown"