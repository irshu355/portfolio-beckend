from datetime import datetime, timedelta


def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = abs(add_days)
    current_date = from_date
    coefficient = 1 if add_days > 0 else -1
    while business_days_to_add > 0:
        current_date += timedelta(days=coefficient * 1)
        weekday = current_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date
