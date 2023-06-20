import pytz


def time_to_utc(naive, timezone="America/Mexico_City"):
    local = pytz.timezone(timezone)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def utc_to_time(naive, timezone="America/Mexico_City"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
