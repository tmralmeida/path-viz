import datetime

def convert_date(date):
    """Convert date to timestamp

    Args:
        date (str): string of the date '%Y-%m-%d %H:%M:%S'

    Returns:
        float: timestamp
    """
    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return datetime.datetime.timestamp(date_time_obj)


