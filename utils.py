from datetime import datetime, date, timedelta

def is_near_expiry(expiry_date, days=3):
    if isinstance(expiry_date, datetime):
        expiry_date = expiry_date.date()
    elif not isinstance(expiry_date, date):
        raise TypeError("expiry_date harus berupa date atau datetime object")

    now = datetime.now().date()
    diff = (expiry_date - now).days
    return 0 <= diff <= days